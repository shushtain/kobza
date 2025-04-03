export function initExChoice() {
  const tasks = document.querySelectorAll(".ex-choice .task");

  tasks.forEach((task) => {
    // Get all answer buttons and shuffle them
    const answers = task.querySelector(".a");
    const buttons = Array.from(answers.children);

    if (!task.classList.contains("no-shuffle")) {
      // Fisher-Yates shuffle
      for (let i = buttons.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        answers.appendChild(buttons[j]);
      }
    }

    // Add click handlers to buttons
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        // Only handle click if not already revealed
        if (!buttons[0].classList.contains("revealed")) {
          buttons.forEach((b) => b.classList.add("revealed"));

          // Add false class if clicked button isn't true
          if (!button.classList.contains("true")) {
            button.classList.add("false");
          }
        }
      });
    });
  });
}
