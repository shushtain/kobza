// FLASHCARDS
class FlashcardViewer {
  constructor(container) {
    this.container = container;
    this.cards = this.getCards();
    this.currentIndex = 0;
    this.isFlipped = false;

    // Cache DOM elements
    this.cardInner = container.querySelector(".inner");
    this.cardFront = container.querySelector(".front");
    this.cardBack = container.querySelector(".back");
    this.counter = container.querySelector(".counter");
    this.window = container.querySelector(".window");

    // Bind controls
    container.querySelector(".button.prev").addEventListener("click", (e) => {
      e.preventDefault();
      this.prev();
      this.window.focus();
    });
    container.querySelector(".button.next").addEventListener("click", (e) => {
      e.preventDefault();
      this.next();
      this.window.focus();
    });
    container.querySelector(".button.flip").addEventListener("click", (e) => {
      e.preventDefault();
      this.flip();
      this.window.focus();
    });
    container
      .querySelector(".button.restart")
      .addEventListener("click", (e) => {
        e.preventDefault();
        this.restart();
        this.window.focus();
      });

    // Add click event to window
    this.window.addEventListener("click", (e) => {
      e.preventDefault();
      this.flip();
      this.window.focus();
    });

    // Add keyboard control
    this.window.addEventListener("keydown", (e) => {
      if (e.code === "Space") {
        e.preventDefault();
        this.flip();
      }
      if (e.code === "ArrowRight") {
        e.preventDefault();
        this.next();
      }
      if (e.code === "ArrowLeft") {
        e.preventDefault();
        this.prev();
      }
    });

    // Initialize
    this.updateCard();
  }

  getCards() {
    return Array.from(
      this.container.querySelectorAll(".flashcards .flashcard")
    ).map((card) => ({
      question: card.querySelector("dt").textContent,
      answer: card.querySelector("dd").textContent,
      image: card.querySelector("img").src,
    }));
  }

  updateCard() {
    const card = this.cards[this.currentIndex];
    this.cardFront.innerHTML = `
      <img src="${card.image}" alt="">
      <h3>${card.question}</h3>
    `;
    this.cardBack.innerHTML = `
      <img src="${card.image}" alt="">
      <p>${card.answer}</p>
    `;
    this.counter.textContent = `${this.currentIndex + 1}/${this.cards.length}`;
    this.isFlipped = false;
    this.cardInner.classList.remove("flipped");
  }

  next() {
    if (this.currentIndex < this.cards.length - 1) {
      this.currentIndex++;
      this.updateCard();
    }
  }

  prev() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.updateCard();
    }
  }

  flip() {
    this.isFlipped = !this.isFlipped;
    this.cardInner.classList.toggle("flipped");
  }

  restart() {
    this.currentIndex = 0;
    this.updateCard();
  }
}

// Initialize all flashcard viewers on the page
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".flashcards-wrapper").forEach((container) => {
    new FlashcardViewer(container);
  });
});

// ORDERWORDS

const orderwords = document.querySelectorAll(".ex-ow-task");

orderwords.forEach((orderwordsLine) => {
  const items = orderwordsLine.querySelectorAll(".draggable");
  let draggedItem = null;

  let correctOrder = [];

  items.forEach((item) => {
    correctOrder.push(item.innerHTML);

    item.addEventListener("dragstart", (e) => {
      draggedItem = item;
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/html", item.outerHTML);
    });

    item.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    item.addEventListener("drop", (e) => {
      e.preventDefault();
      if (item !== draggedItem) {
        const draggedIndex = Array.from(orderwordsLine.children).indexOf(
          draggedItem
        );
        const targetIndex = Array.from(orderwordsLine.children).indexOf(item);
        orderwordsLine.insertBefore(
          draggedItem,
          targetIndex > draggedIndex ? item.nextSibling : item
        );
        orderwordsCheck(orderwordsLine);
      }
    });
    item.setAttribute("draggable", true);
  });

  orderwordsLine.setAttribute("data-correct-order", correctOrder.join(","));

  let newOrder = Array.from(items);

  for (let i = newOrder.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newOrder[i], newOrder[j]] = [newOrder[j], newOrder[i]];
  }

  orderwordsLine.innerHTML = "";

  newOrder.forEach((item) => {
    orderwordsLine.appendChild(item);
  });
});

function orderwordsCheck(line) {
  const items = line.querySelectorAll(".draggable");
  let currentOrder = [];

  items.forEach((item) => {
    currentOrder.push(item.innerHTML);
  });

  if (currentOrder.join(",") === line.getAttribute("data-correct-order")) {
    line.classList.add("success");
  } else {
    line.classList.remove("success");
  }
}

// MATCHPICTURES

const matchpictures = document.querySelectorAll(".ex-mp-task");

matchpictures.forEach((matchpicture) => {
  const items = matchpicture.querySelectorAll(".draggable");
  let draggedItem = null;

  let correctOrder = [];

  items.forEach((item) => {
    correctOrder.push(item.innerHTML);

    item.addEventListener("dragstart", (e) => {
      draggedItem = item;
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/html", item.outerHTML);
    });

    item.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    item.addEventListener("drop", (e) => {
      e.preventDefault();
      if (item !== draggedItem) {
        const draggedIndex = Array.from(matchpicture.children).indexOf(
          draggedItem
        );
        const targetIndex = Array.from(matchpicture.children).indexOf(item);
        matchpicture.insertBefore(
          draggedItem,
          targetIndex > draggedIndex ? item.nextSibling : item
        );
        mpCheck(matchpicture);
      }
    });
    item.setAttribute("draggable", true);
  });

  matchpicture.setAttribute("data-correct-order", correctOrder.join(","));

  let newOrder = Array.from(items);

  for (let i = newOrder.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newOrder[i], newOrder[j]] = [newOrder[j], newOrder[i]];
  }

  matchpicture.innerHTML = "";

  newOrder.forEach((item) => {
    matchpicture.appendChild(item);
  });
});

function mpCheck(line) {
  const items = line.querySelectorAll(".draggable");
  let currentOrder = [];

  items.forEach((item) => {
    currentOrder.push(item.innerHTML);
  });

  if (currentOrder.join(",") === line.getAttribute("data-correct-order")) {
    line.classList.add("success");
  } else {
    line.classList.remove("success");
  }
}
