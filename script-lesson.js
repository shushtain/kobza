// MAIN INITIALIZATION
// ===
// ==
// =

document.addEventListener("DOMContentLoaded", () => {
  initFlashcards();
  initExChoice();
  initExFill();
  initExFormat();
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
  const toggleFlashcards = document.querySelector(".toggle-flashcards");
  let isAllRevealed = false;

  let timing = 200;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    timing = 0;
  }

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
    const toggleDefinitions = createCardToggler(card, timing);

    card.addEventListener("click", () => toggleDefinitions());
    card.addEventListener("keydown", (e) => {
      if (e.code === "Enter" || e.code === "Space") {
        e.preventDefault();
        toggleDefinitions();
      }
    });

    card.toggleDefinitions = toggleDefinitions;
  });

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

    // Fisher-Yates shuffle
    for (let i = buttons.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      answers.appendChild(buttons[j]);
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
// EX-FILL
// ===
// ==
// =

function initExFill() {
  const buttons = document.querySelectorAll(".ex-fill button");

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
