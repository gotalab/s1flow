// Bench tables: select a column heading to sort by it, and filter long tables by candidate.
// The Markdown stays a plain table; this reads the numbers back out of the cells.
(() => {
  const LOWER_IS_BETTER = /latency|cost|ece|brier|mae|loss|false alarms|refused/i;

  function number(cell) {
    const match = cell.textContent.replace(/,/g, "").match(/-?\d+(\.\d+)?/);
    return match ? parseFloat(match[0]) : null;
  }

  function sortable(table) {
    const body = table.tBodies[0];
    const heads = [...table.tHead.rows[0].cells];
    heads.forEach((th, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "bench-sort";
      button.append(...th.childNodes);
      th.append(button);
      button.addEventListener("click", () => {
        const text = index === 0;
        const ascendingFirst = text || LOWER_IS_BETTER.test(button.textContent);
        const current = th.getAttribute("aria-sort");
        const first = ascendingFirst ? "ascending" : "descending";
        const next = current === first ? (first === "ascending" ? "descending" : "ascending") : first;
        heads.forEach((h) => h.removeAttribute("aria-sort"));
        th.setAttribute("aria-sort", next);
        const sign = next === "ascending" ? 1 : -1;
        const rows = [...body.rows].map((row) => {
          const cell = row.cells[index];
          return { row, key: text ? cell.textContent.trim().toLowerCase() : number(cell) };
        });
        rows.sort((a, b) => {
          if (a.key === null || a.key === "") return b.key === null || b.key === "" ? 0 : 1;  // empty last, always
          if (b.key === null || b.key === "") return -1;
          return a.key < b.key ? -sign : a.key > b.key ? sign : 0;
        });
        body.append(...rows.map((r) => r.row));
      });
    });
  }

  function filterable(table) {
    const rows = [...table.tBodies[0].rows];
    const label = document.createElement("label");
    label.className = "bench-filter";
    const input = document.createElement("input");
    input.type = "search";
    input.placeholder = "Filter candidates";
    input.setAttribute("aria-label", "Filter candidates");
    const count = document.createElement("span");
    count.setAttribute("aria-live", "polite");
    label.append(input, count);
    table.closest(".md-typeset__scrollwrap, .bench").before(label);
    input.addEventListener("input", () => {
      const terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      let shown = 0;
      rows.forEach((row) => {
        const name = row.cells[0].textContent.toLowerCase();
        const hit = terms.length === 0 || terms.some((t) => name.includes(t));
        row.hidden = !hit;
        shown += hit;
      });
      count.textContent = terms.length ? `${shown} of ${rows.length}` : "";
    });
  }

  function init() {
    document.querySelectorAll(".md-typeset .bench table").forEach((table) => {
      if (table.dataset.benchReady || !table.tHead || !table.tBodies[0]) return;
      table.dataset.benchReady = "1";
      sortable(table);
      if (table.tBodies[0].rows.length >= 12) filterable(table);
    });
  }

  if (window.document$) window.document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
