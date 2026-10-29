"""A repository's GitHub history as data: fetch it, see how its labels are used, and why a case got its label.

`s1flow github fetch owner/repo`      -> data/raw/github/<owner>__<repo>/{issues,prs}.jsonl, labels.json
`s1flow github audit owner/repo`      -> how labels are used today, and by whom (audit.md)
`s1flow github rationale owner/repo --id TASK` -> each row of tasks/TASK/data.jsonl gets the maintainers' comments
                                                 around its labelling as `rationale` (GEPA's reflection LM reads it)

Turning the fetched issues into a task (data.jsonl and task.py) is the agent's step, as the Skill's collect
reference says: which issues are one decision, and what the criteria are, is decided with the user.

Everything goes through `gh api graphql` with the user's own login. GraphQL allows
5,000 points an hour; a page here costs one or two. Pages are appended as they
arrive and the cursor is saved, so an interrupted fetch resumes where it stopped.
"""

from __future__ import annotations

import collections
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from ..core.errors import ConfigError, NotFound
from ..project import Project

GH_MISSING = "s1flow github calls GitHub through the GitHub CLI: install gh (https://cli.github.com) and run gh auth login"


def require_gh() -> None:
    """The GitHub CLI, or one line saying what to install."""
    if shutil.which("gh") is None:
        raise ConfigError(GH_MISSING)


BOT_SUFFIXES = ("[bot]", "-bot", "bot")
BODY_CHARS = 4000

ISSUES = """
query($owner: String!, $name: String!, $first: Int!, $after: String) {
  rateLimit { cost remaining resetAt }
  repository(owner: $owner, name: $name) {
    issues(first: $first, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title body createdAt closedAt state stateReason authorAssociation
        author { login __typename }
        labels(first: 20) { nodes { name } }
        timelineItems(first: 40, itemTypes: [LABELED_EVENT, UNLABELED_EVENT, MARKED_AS_DUPLICATE_EVENT]) {
          nodes {
            __typename
            ... on LabeledEvent { createdAt label { name } actor { login __typename } }
            ... on UnlabeledEvent { createdAt label { name } actor { login __typename } }
            ... on MarkedAsDuplicateEvent { createdAt canonical { ... on Issue { number } } }
          }
        }
      }
    }
  }
}"""

PRS = """
query($owner: String!, $name: String!, $first: Int!, $after: String) {
  rateLimit { cost remaining resetAt }
  repository(owner: $owner, name: $name) {
    pullRequests(first: $first, after: $after, states: MERGED, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title body createdAt mergedAt authorAssociation additions deletions changedFiles
        author { login __typename }
        labels(first: 20) { nodes { name } }
        files(first: 60) { nodes { path additions deletions } }
        reviews(first: 50) { totalCount nodes { state submittedAt author { login } } }
        commits(first: 100) { totalCount nodes { commit { committedDate } } }
      }
    }
  }
}"""

LABELS = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) { labels(first: 100) { nodes { name description } } }
}"""


def repo_dir(project: Project, repo: str) -> Path:
    return project.root / "data" / "raw" / "github" / repo.replace("/", "__")


def is_bot(actor: dict[str, Any] | None) -> bool:
    if not actor:
        return True  # a deleted account or an app without a login
    login = (actor.get("login") or "").lower()
    return actor.get("__typename") == "Bot" or login.endswith(BOT_SUFFIXES) or login == "github-actions"


def graphql(query: str, variables: dict[str, Any], attempts: int = 6) -> dict[str, Any]:
    """One `gh api graphql` call, retried on GitHub's transient 502s and secondary limits."""
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if v is not None:
            args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    for attempt in range(attempts):
        p = subprocess.run(args, capture_output=True, text=True)
        if p.returncode == 0:
            data = json.loads(p.stdout)
            if data.get("errors"):
                raise RuntimeError(json.dumps(data["errors"])[:500])
            return data["data"]
        err = (p.stderr + p.stdout)[:300]
        if "secondary rate limit" in err.lower():
            time.sleep(60)
        elif attempt == attempts - 1:
            raise RuntimeError(f"gh api graphql failed: {err}")
        else:
            time.sleep(2 * 2**attempt)
    raise AssertionError("unreachable")


def _pace(rate: dict[str, Any]) -> None:
    """Stop short of the hourly budget instead of running into it."""
    if rate["remaining"] < 200:
        reset = time.mktime(time.strptime(rate["resetAt"], "%Y-%m-%dT%H:%M:%SZ")) - time.timezone
        time.sleep(max(0.0, reset - time.time()) + 5)


def fetch(project: Project, repo: str, kind: str, limit: int, page: int) -> int:
    """Append up to `limit` issues or merged PRs (newest first). Returns how many are stored."""
    owner, name = repo.split("/")
    out = repo_dir(project, repo)
    out.mkdir(parents=True, exist_ok=True)
    path, state_path = out / f"{kind}.jsonl", out / f"{kind}.cursor.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"after": None, "done": False}
    have = sum(1 for _ in path.open()) if path.exists() else 0
    query, field = (ISSUES, "issues") if kind == "issues" else (PRS, "pullRequests")
    while have < limit and not state["done"]:
        n = min(page, limit - have)
        try:
            data = graphql(query, {"owner": owner, "name": name, "first": n, "after": state["after"]})
        except RuntimeError:
            if page <= 5:
                raise
            page //= 2  # big pages of nested connections time out on GitHub's side
            continue
        conn = data["repository"][field]
        with path.open("a") as f:
            for node in conn["nodes"]:
                if node.get("body"):
                    node["body"] = node["body"][:BODY_CHARS]
                f.write(json.dumps(node, ensure_ascii=False) + "\n")
        have += len(conn["nodes"])
        state = {"after": conn["pageInfo"]["endCursor"], "done": not conn["pageInfo"]["hasNextPage"]}
        state_path.write_text(json.dumps(state))
        _pace(data["rateLimit"])
    if not (out / "labels.json").exists():
        labels = graphql(LABELS, {"owner": owner, "name": name})["repository"]["labels"]["nodes"]
        (out / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1))
    return have


def load(project: Project, repo: str, kind: str) -> list[dict[str, Any]]:
    path = repo_dir(project, repo) / f"{kind}.jsonl"
    if not path.exists():
        raise NotFound(f"nothing fetched from {repo} yet ({path}): run s1flow github fetch {repo} first")
    seen, rows = set(), []
    for line in path.read_text().split("\n"):
        if line.strip():
            r = json.loads(line)
            if r["number"] not in seen:
                seen.add(r["number"])
                rows.append(r)
    return rows


def label_descriptions(project: Project, repo: str) -> dict[str, str]:
    path = repo_dir(project, repo) / "labels.json"
    return {l["name"]: l.get("description") or "" for l in json.loads(path.read_text())} if path.exists() else {}


def group_of(label: str) -> str:
    return label.split("/", 1)[0] if "/" in label else "(no prefix)"


def labelled_by(issue: dict[str, Any]) -> dict[str, str]:
    """Current label -> 'human' or 'bot', from who applied it last."""
    who: dict[str, str] = {}
    for ev in issue.get("timelineItems", {}).get("nodes", []):
        if ev.get("__typename") == "LabeledEvent" and ev.get("label"):
            who[ev["label"]["name"]] = "bot" if is_bot(ev.get("actor")) else "human"
    return {l["name"]: who.get(l["name"], "unknown") for l in issue["labels"]["nodes"]}


# ---------- audit ----------


def audit(project: Project, repo: str) -> str:
    issues = load(project, repo, "issues")
    descs = label_descriptions(project, repo)
    n = len(issues)
    unlabeled = sum(1 for i in issues if not i["labels"]["nodes"])
    groups: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    covered: collections.Counter = collections.Counter()
    multi: collections.Counter = collections.Counter()
    by: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for i in issues:
        who = labelled_by(i)
        per_group = collections.Counter(group_of(l) for l in who)
        for g, k in per_group.items():
            covered[g] += 1
            multi[g] += k > 1
        for l, w in who.items():
            groups[group_of(l)][l] += 1
            by[group_of(l)][w] += 1
    dupes = sum(1 for i in issues if i.get("stateReason") == "DUPLICATE")
    first, last = issues[-1]["createdAt"][:10], issues[0]["createdAt"][:10]
    L = [
        f"# {repo} · how labels are used",
        "",
        f"{n} issues ({first} to {last}). Unlabelled {unlabeled} ({unlabeled / n:.0%}). Closed as duplicates {dupes}.",
        "",
        "| group | issues with one | with two or more | applied by a person / bot / unknown | most used labels |",
        "|---|---|---|---|---|",
    ]
    for g, c in sorted(groups.items(), key=lambda kv: -covered[kv[0]]):
        b = by[g]
        top = ", ".join(f"{l} ({k})" for l, k in c.most_common(6))
        L.append(f"| {g} | {covered[g]} ({covered[g] / n:.0%}) | {multi[g]} | {b['human']} / {b['bot']} / {b['unknown']} | {top} |")
    missing = [l for l in sorted(descs) if not descs[l]]
    L += ["", f"{len(missing)} labels without a description: " + ", ".join(missing[:40])]
    md = "\n".join(L) + "\n"
    (repo_dir(project, repo) / "audit.md").write_text(md)
    return md


# ---------- why a case got its label (for the reflection LM only) ----------

MAINTAINERS = {"OWNER", "MEMBER", "COLLABORATOR"}
BOILERPLATE = ("reserving self-assignment",)  # bot replies unrelated to the decision


def fetch_comments(project: Project, repo: str, numbers: list[int], per_query: int = 20) -> dict[int, list[dict[str, Any]]]:
    """Comments of the given issues, cached in comments.jsonl. Aliased queries fetch 20 issues at a time."""
    owner, name = repo.split("/")
    path = repo_dir(project, repo) / "comments.jsonl"
    have: dict[int, list[dict[str, Any]]] = {}
    if path.exists():
        for line in path.read_text().split("\n"):
            if line.strip():
                r = json.loads(line)
                have[r["number"]] = r["comments"]
    todo = [n for n in numbers if n not in have]
    fields = "comments(first: 30) { nodes { createdAt authorAssociation body author { login __typename } } }"
    for k in range(0, len(todo), per_query):
        chunk = todo[k : k + per_query]
        parts = " ".join(f"i{n}: issue(number: {n}) {{ number {fields} }}" for n in chunk)
        q = f"query($owner: String!, $name: String!) {{ rateLimit {{ cost remaining resetAt }} repository(owner: $owner, name: $name) {{ {parts} }} }}"
        data = graphql(q, {"owner": owner, "name": name})
        with path.open("a") as f:
            for n in chunk:
                node = data["repository"].get(f"i{n}") or {"comments": {"nodes": []}}
                cs = node["comments"]["nodes"]
                for c in cs:
                    c["body"] = (c.get("body") or "")[:1500]
                have[n] = cs
                f.write(json.dumps({"number": n, "comments": cs}, ensure_ascii=False) + "\n")
        _pace(data["rateLimit"])
    return have


def label_time(issue: dict[str, Any], label: str) -> str | None:
    times = [
        ev["createdAt"]
        for ev in issue.get("timelineItems", {}).get("nodes", [])
        if ev.get("__typename") == "LabeledEvent" and (ev.get("label") or {}).get("name") == label
    ]
    return max(times) if times else None


def rationale(issue: dict[str, Any], label: str, comments: list[dict[str, Any]], within_hours: float = 24, chars: int = 400) -> str:
    """What maintainers or bots wrote up to a day after `label` was applied: the reasons, when given."""
    t = label_time(issue, label)
    if not t:
        return ""
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.mktime(time.strptime(t, "%Y-%m-%dT%H:%M:%SZ")) - time.timezone + within_hours * 3600))
    reporter = (issue.get("author") or {}).get("login")
    picked = [
        c for c in comments
        if c["createdAt"] <= cutoff and (c.get("author") or {}).get("login") != reporter
        and (c.get("authorAssociation") in MAINTAINERS or is_bot(c.get("author")))
        and not any(b in c["body"] for b in BOILERPLATE)
    ]
    return " / ".join(" ".join(c["body"].split())[:chars] for c in picked[-3:])


def add_rationales(project: Project, repo: str, task_id: str) -> tuple[int, int]:
    """Fill `rationale` on a GitHub task's rows from the comments around their labelling."""
    d = project.tasks_dir / task_id
    rows = [json.loads(l) for l in (d / "data.jsonl").read_text().split("\n") if l.strip()]
    issues = {i["number"]: i for i in load(project, repo, "issues")}
    numbers = [int(r["id"].lstrip("#")) for r in rows]
    comments = fetch_comments(project, repo, numbers)
    filled = 0
    for r, n in zip(rows, numbers):
        why = rationale(issues[n], str(r["label"]), comments.get(n, [])) if n in issues else ""
        r["rationale"] = why
        filled += bool(why)
    (d / "data.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    return filled, len(rows)
