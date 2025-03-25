// MAIN INITIALIZATION
// ===
// ==
// =

document.addEventListener("DOMContentLoaded", () => {
  initFlashcards();
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

// util
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
