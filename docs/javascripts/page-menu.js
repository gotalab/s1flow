// The page actions menu closes on a choice, a click outside it, or Escape.
document.addEventListener("click", (event) => {
  for (const menu of document.querySelectorAll("details.page-menu[open]")) {
    const inside = menu.contains(event.target);
    if (!inside || event.target.closest(".page-menu__list button, .page-menu__list a")) menu.open = false;
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") document.querySelectorAll("details.page-menu[open]").forEach((menu) => (menu.open = false));
});
