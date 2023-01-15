const toggleBtn = document.querySelector(".navbar__toggleBtn");
const menu = document.querySelector(".navbar__menu");
const toggle_munu = document.querySelector(".menu_toggle");

toggleBtn.addEventListener("click", () => {
    menu.classList.toggle("active");
    toggle_munu.className += "toggleActive";
});
