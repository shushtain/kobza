export function initExGaps() {
  const buttons = document.querySelectorAll(".ex-gaps button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      if (!button.classList.contains("revealed")) {
        button.classList.add("revealed");
      }
    });
  });
}
