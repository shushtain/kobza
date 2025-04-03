export function initExFormat() {
  const buttons = document.querySelectorAll(".ex-format button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      if (!button.classList.contains("revealed")) {
        button.classList.add("revealed");
      }
    });
  });
}
