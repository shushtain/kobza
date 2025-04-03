export function initExOrder() {
  const tasks = document.querySelectorAll(".ex-order .task");

  tasks.forEach((task) => {
    // Store initial sequence
    const buttons = Array.from(task.querySelectorAll("button"));
    const initialSequence = buttons
      .map((btn) => btn.textContent.trim())
      .join("|");
    task.dataset.sequence = initialSequence;

    // Fisher-Yates shuffle
    for (let i = buttons.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      task.appendChild(buttons[j]);
    }

    // Add drag handlers
    buttons.forEach((btn) => {
      btn.draggable = true;

      btn.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("text/plain", ""); // Required for Firefox
        e.target.classList.add("dragging");
      });

      btn.addEventListener("dragend", (e) => {
        e.target.classList.remove("dragging");
        checkSequence(task);
      });

      btn.addEventListener("dragover", (e) => {
        e.preventDefault();
      });

      btn.addEventListener("drop", (e) => {
        e.preventDefault();
        const dragging = task.querySelector(".dragging");
        if (dragging && dragging !== btn) {
          const buttons = [...task.querySelectorAll("button")];
          const dragPos = buttons.indexOf(dragging);
          const dropPos = buttons.indexOf(btn);

          if (dragPos < dropPos) {
            btn.parentNode.insertBefore(dragging, btn.nextSibling);
          } else {
            btn.parentNode.insertBefore(dragging, btn);
          }
          checkSequence(task);
        }
      });

      // Add keyboard handlers
      btn.addEventListener("keydown", (e) => {
        const buttons = [...task.querySelectorAll("button")];
        const currentIndex = buttons.indexOf(btn);

        switch (e.key) {
          case "ArrowLeft":
            if (e.ctrlKey) {
              if (currentIndex > 0) {
                e.preventDefault();
                task.insertBefore(btn, buttons[0]);
                btn.focus();
                checkSequence(task);
              }
            } else if (currentIndex > 0) {
              e.preventDefault();
              task.insertBefore(btn, buttons[currentIndex - 1]);
              btn.focus();
              checkSequence(task);
            }
            break;
          case "ArrowRight":
            if (e.ctrlKey) {
              if (currentIndex < buttons.length - 1) {
                e.preventDefault();
                task.appendChild(btn);
                btn.focus();
                checkSequence(task);
              }
            } else if (currentIndex < buttons.length - 1) {
              e.preventDefault();
              task.insertBefore(btn, buttons[currentIndex + 1].nextSibling);
              btn.focus();
              checkSequence(task);
            }
            break;
        }
      });
    });
  });
}

function checkSequence(task) {
  const currentSequence = Array.from(task.querySelectorAll("button"))
    .map((btn) => btn.textContent.trim())
    .join("|");

  if (currentSequence === task.dataset.sequence) {
    task.classList.add("correct");
  } else {
    task.classList.remove("correct");
  }
}
