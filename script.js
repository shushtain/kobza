// ORDERWORDS

const orderwords = document.querySelectorAll(".orderwords-line");

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
    line.classList.add("orderwords-success");
  } else {
    line.classList.remove("orderwords-success");
  }
}

// MATCHPICTURES

const matchpictures = document.querySelectorAll(".mp-phrases");

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
    line.classList.add("mp-success");
  } else {
    line.classList.remove("mp-success");
  }
}
