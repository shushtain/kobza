// Global values

let dur01 = 100;
let dur02 = 200;

// =
// ==
// ===
// MAIN INITIALIZATION
// ===
// ==
// =

document.addEventListener("DOMContentLoaded", () => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    dur01 = 0;
    dur02 = 0;
  }

  initFlashcards();
  initExChoice();
  initExGaps();
  initExFormat();
  initExOrder();
  initExPref();
  initExFacts();
});

// =
// ==
// ===
// FLASHCARDS
// ===
// ==
// =

// init
function initFlashcards() {
  const flashcards = document.querySelectorAll(".flashcard");
  const controls = document.querySelector(".flashcards-wrapper .controls");
  const toggleFlashcards = document.querySelector(".toggle-flashcards");
  let isAllRevealed = false;

  // setup for dd
  flashcards.forEach((card) => {
    const definitions = card.querySelectorAll("dd");
    definitions.forEach((dd) => {
      dd.style.opacity = "0";
      dd.style.maxHeight = "0";
      dd.style.visibility = "hidden";
    });
  });

  // setup for cards
  flashcards.forEach((card) => {
    const toggleDefinitions = createCardToggler(card, dur02);

    card.addEventListener("click", () => toggleDefinitions());
    card.addEventListener("keydown", (e) => {
      if (e.code === "Enter" || e.code === "Space") {
        e.preventDefault();
        toggleDefinitions();
      }
    });

    card.toggleDefinitions = toggleDefinitions;
  });

  // show controls
  controls.style.display = "flex";

  // reveal-all function
  toggleFlashcards.addEventListener("click", () => {
    isAllRevealed = !isAllRevealed;
    flashcards.forEach((card) => card.toggleDefinitions(isAllRevealed));
    toggleFlashcards.querySelector("span").textContent = isAllRevealed
      ? "Hide answers"
      : "Show answers";
    toggleFlashcards.classList.toggle("toggled");
  });
}

// switch logic
function createCardToggler(card, timing) {
  const definitions = card.querySelectorAll("dd");
  let isRevealed = false;

  const toggleDefinitions = (forcedState = null) => {
    if (forcedState === null) {
      isRevealed = !isRevealed;
    } else {
      isRevealed = forcedState;
    }

    definitions.forEach((dd) => {
      if (isRevealed) {
        dd.style.visibility = "visible";
        dd.style.maxHeight = `${dd.scrollHeight}px`;
        setTimeout(() => {
          if (isRevealed) {
            dd.style.opacity = "1";
          }
        }, timing);
      } else {
        dd.style.opacity = "0";
        setTimeout(() => {
          if (!isRevealed) {
            dd.style.maxHeight = "0";
          }
        }, timing);
        setTimeout(() => {
          if (!isRevealed) {
            dd.style.visibility = "hidden";
          }
        }, timing);
      }
    });
  };

  return toggleDefinitions;
}

// =
// ==
// ===
// EX-CHOICE
// ===
// ==
// =

function initExChoice() {
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

// =
// ==
// ===
// EX-GAPS
// ===
// ==
// =

function initExGaps() {
  const buttons = document.querySelectorAll(".ex-gaps button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      if (!button.classList.contains("revealed")) {
        button.classList.add("revealed");
      }
    });
  });
}

// =
// ==
// ===
// EX-FORMAT
// ===
// ==
// =

function initExFormat() {
  const buttons = document.querySelectorAll(".ex-format button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      if (!button.classList.contains("revealed")) {
        button.classList.add("revealed");
      }
    });
  });
}

// =
// ==
// ===
// EX-ORDER
// ===
// ==
// =

function initExOrder() {
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

// =
// ==
// ===
// EX-PREF
// ===
// ==
// =

function initExPref() {
  const tasks = document.querySelectorAll(".ex-pref .task");

  tasks.forEach((task) => {
    const box = task.querySelector(".box");
    const dialog = task.querySelector("dialog");
    const closeBtn = dialog.querySelector(".close");
    const likeBtn = dialog.querySelector(".like");
    const dislikeBtn = dialog.querySelector(".dislike");

    // Open dialog
    box.addEventListener("click", () => {
      dialog.showModal();
      setTimeout(() => {
        dialog.classList.add("open");
      }, dur01);
      box.classList.add("revealed");
    });

    // Close dialog
    closeBtn.addEventListener("click", () => {
      dialog.classList.remove("open");
      setTimeout(() => {
        dialog.close();
      }, dur01);
    });

    // Close on click outside
    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) {
        dialog.classList.remove("open");
        setTimeout(() => {
          dialog.close();
        }, dur01);
      }
    });

    // Handle like/dislike
    [likeBtn, dislikeBtn].forEach((btn) => {
      btn.addEventListener("click", () => {
        if (!likeBtn.classList.contains("revealed")) {
          likeBtn.classList.add("revealed");
          dislikeBtn.classList.add("revealed");
          btn.classList.add("selected");
          if (btn == likeBtn) {
            box.classList.add("like");
          } else {
            box.classList.add("dislike");
          }
        }
      });
    });
  });
}

// =
// ==
// ===
// EX-FACTS
// ===
// ==
// =

function initExFacts() {
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
      }, dur02);
      box.classList.add("revealed");
    });

    // Close dialog
    closeBtn.addEventListener("click", () => {
      dialog.classList.remove("open");
      setTimeout(() => {
        dialog.close();
      }, dur02);
    });

    // Close on click outside
    dialog.addEventListener("click", (e) => {
      if (e.target === dialog) {
        dialog.classList.remove("open");
        setTimeout(() => {
          dialog.close();
        }, dur02);
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
