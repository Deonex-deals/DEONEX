window.addEventListener("load", () => {
  const loader = document.getElementById("page-loader");

  setTimeout(() => {
    if (loader) {
      loader.classList.add("hidden");
    }
  }, 650);
});

const menuToggle = document.getElementById("menu-toggle");
const mainNav = document.getElementById("main-nav");

if (menuToggle && mainNav) {
  menuToggle.addEventListener("click", () => {
    mainNav.classList.toggle("open");
  });
}
