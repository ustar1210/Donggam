const toggleBtn = document.querySelector(".navbar__toggleBtn");
const menu = document.querySelector(".navbar__menu");
const admin_menu = document.querySelector(".navbar__menu_admin");
const toggle_munu = document.querySelector(".menu_toggle");

toggleBtn.addEventListener("click", () => {
    menu.classList.toggle("active");
    toggle_munu.className += "toggleActive";
});
