import { getDurations } from "./lesson/utils.js";
import { initFlashcards } from "./lesson/flashcards.js";
import { initExChoice } from "./lesson/ex-choice.js";
import { initExGaps } from "./lesson/ex-gaps.js";
import { initExFormat } from "./lesson/ex-format.js";
import { initExOrder } from "./lesson/ex-order.js";
import { initExPref } from "./lesson/ex-pref.js";
import { initExFacts } from "./lesson/ex-facts.js";

document.addEventListener("DOMContentLoaded", () => {
  const durs = getDurations();
  initFlashcards(durs.dur02);
  initExChoice();
  initExGaps();
  initExFormat();
  initExOrder();
  initExPref(durs.dur01);
  initExFacts(durs.dur01);
});
