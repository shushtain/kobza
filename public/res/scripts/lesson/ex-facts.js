export function initExFacts(timing) {
  const tasks = document.querySelectorAll(".ex-facts .task");

  tasks.forEach((task) => {
    const box = task.querySelector(".box");
    const dialog = task.querySelector("dialog");
    const closeBtn = dialog.querySelector(".close");
    const trueBtn = dialog.querySelector("button:last-of-type");
    const falseBtn = dialog.querySelector("button:first-of-type");

    // Open dialog
    box.addEventListener("click", () => {
      dialog.showModal();
      setTimeout(() => {
        dialog.classList.add("open");
      }, timing);
      box.classList.add("revealed");
    });

    // Close dialog
    closeBtn.addEventListener("click", () => {
      dialog.classList.remove("open");
      setTimeout(() => {
        dialog.close();
      }, timing);
    });

    // Close on click outside
    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) {
        dialog.classList.remove("open");
        setTimeout(() => {
          dialog.close();
        }, timing);
      }
    });

    // Handle true/false buttons
    [trueBtn, falseBtn].forEach((btn) => {
      btn.addEventListener("click", () => {
        if (!trueBtn.classList.contains("revealed")) {
          trueBtn.classList.add("revealed");
          falseBtn.classList.add("revealed");

          // Add false class if clicked button isn't true
          if (!btn.classList.contains("true")) {
            box.classList.add("false");
            btn.classList.add("false");
          } else {
            box.classList.add("true");
          }
        }
      });
    });
  });
}
