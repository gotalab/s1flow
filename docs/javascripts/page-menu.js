// The page actions menu closes on a choice, a click outside it, or Escape; Escape returns focus to its toggle.
document.addEventListener("click", (event) => {
  for (const menu of document.querySelectorAll("details.page-menu[open]")) {
    const inside = menu.contains(event.target);
    if (!inside || event.target.closest(".page-menu__list button, .page-menu__list a")) menu.open = false;
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  for (const menu of document.querySelectorAll("details.page-menu[open]")) {
    const hadFocus = menu.contains(document.activeElement);
    menu.open = false;
    if (hadFocus) menu.querySelector("summary").focus();
  }
});
