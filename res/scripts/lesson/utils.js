export function getDurations() {
  const isReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  return {
    dur01: isReducedMotion ? 0 : 100,
    dur02: isReducedMotion ? 0 : 200,
    dur03: isReducedMotion ? 0 : 300,
    dur04: isReducedMotion ? 0 : 400,
    dur05: isReducedMotion ? 0 : 500,
    dur06: isReducedMotion ? 0 : 600,
    dur07: isReducedMotion ? 0 : 700,
    dur08: isReducedMotion ? 0 : 800,
    dur09: isReducedMotion ? 0 : 900,
    dur10: isReducedMotion ? 0 : 1000,
  };
}
