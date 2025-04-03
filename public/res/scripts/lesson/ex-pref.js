export function initExPref(timing) {
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
