// INIT

const root = document.documentElement;

// THEME TOGGLING

// initialize
if (!root.hasAttribute("data-theme")) {
  let initialTheme = "light";

  // Check system theme
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
  if (systemTheme === "dark") {
    initialTheme = "dark";
  }

  const cachedTheme = localStorage.getItem("theme");
  if (cachedTheme) {
    initialTheme = cachedTheme;
  }
  root.setAttribute("data-theme", initialTheme);
}

// change
const toggleTheme = document.getElementById("toggle-theme");

toggleTheme.addEventListener("click", () => {
  const currentTheme = root.getAttribute("data-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";
  localStorage.setItem("theme", newTheme);
  root.setAttribute("data-theme", newTheme);
});

// fix for flickering
root.style.setProperty("--dur-switch", "0");
window.addEventListener("load", () => {
  setTimeout(() => {
    root.style.setProperty("--dur-switch", "1");
  }, 1);
});
