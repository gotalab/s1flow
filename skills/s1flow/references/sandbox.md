# In a sandbox

In a cloud agent or CI, keys are environment variables and the network may reach only allow-listed
hosts. Before the first model call, run the read-only check:

```bash
s1flow doctor --models a,b --reach
s1flow doctor --policy TASK --connections s1flow.toml --reach
```

It names the variables and hosts a declared connection needs, without printing secret values. A
missing key or blocked host is a setup issue: tell the operator the name from `doctor` and configure
the workflow or sandbox explicitly. A sandbox whose proxy adds the key on the way out (a network secret,
such as Claude Code's cloud environments) keeps it out of the environment, so `doctor` reports it as not
set; leave the variable unset there, and confirm with one `decide` call instead. s1flow sends without a
key it cannot find, and a 401 or 403 back names the key as missing. Policy execution uses the same trusted file:

```bash
s1flow decide --policy TASK --state @state.json --connections s1flow.toml
```

The file passed to `--connections` grants every connection listed in it, so keep it dedicated to the
application's allowed connections. A policy cannot select an arbitrary provider or import code.

Install dependencies as part of the environment or workflow setup, for example
`uv tool install "s1flow[eval,llm]"` for evaluation and LLM support. `s1flow skill install` only writes
the Skill where agents read it. The runtime SDK never installs packages from a policy or from input
data. A local `.env` is a CLI convenience only: loading is bounded to the selected project/root and
nearest Git ancestor, and the CLI does not replace variables that are already set. The SDK reads
environment variables but never reads `.env` or discovers a project.
