// The language selector opens the same page in the other language. The Japanese pages (/ja/) mirror the English
// ones by path; the pages that exist only in English (Benchmarks, Develop s1flow) lead to the Japanese home.
(() => {
  const ENGLISH_ONLY = /^(benchmarks|development)(\/|$)/;

  function relink() {
    const links = [...document.querySelectorAll("a.md-select__link[hreflang]")];
    const root = (lang) => {
      const link = links.find((a) => a.hreflang === lang);
      return link && new URL(link.dataset.root || link.href, location.href).pathname;
    };
    const en = root("en"), ja = root("ja");
    if (!en || !ja) return;
    const path = location.pathname;
    const here = path.startsWith(ja) ? ja : en;
    const page = path.startsWith(here) ? path.slice(here.length) : "";
    for (const a of links) {
      a.dataset.root = a.dataset.root || (a.hreflang === "ja" ? ja : en);
      const target = a.hreflang === "ja" ? ja : en;
      a.href = target + (target === ja && ENGLISH_ONLY.test(page) ? "" : page) + location.hash;
    }
  }

  if (window.document$) window.document$.subscribe(relink);
  else document.addEventListener("DOMContentLoaded", relink);
})();
