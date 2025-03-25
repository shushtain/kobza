// INIT

const root = document.documentElement;

// THEME TOGGLING

// Disable transitions immediately
root.style.setProperty("--dur-switch", "0");

// Initialize theme immediately
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

// Wait for DOM to be ready before setting up interactive features
document.addEventListener("DOMContentLoaded", () => {
  // Set up theme toggle
  const toggleTheme = document.getElementById("toggle-theme");
  toggleTheme.addEventListener("click", () => {
    const currentTheme = root.getAttribute("data-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    localStorage.setItem("theme", newTheme);
    root.setAttribute("data-theme", newTheme);
  });

  // Enable transitions after initial theme is applied
  setTimeout(() => {
    root.style.setProperty("--dur-switch", "1");
  }, 1000);
});
