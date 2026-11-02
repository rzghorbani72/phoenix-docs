import { useEffect, useState } from "react";

/** Below this width the step panel is a bottom sheet and the toolbar collapses. */
export const NARROW_PX = 860;
const query = `(max-width: ${NARROW_PX - 0.02}px)`;

export function isNarrow() {
  return typeof window !== "undefined" && window.matchMedia(query).matches;
}

export function useNarrow() {
  const [narrow, setNarrow] = useState(isNarrow);
  useEffect(() => {
    const m = window.matchMedia(query);
    const on = () => setNarrow(m.matches);
    m.addEventListener("change", on);
    return () => m.removeEventListener("change", on);
  }, []);
  return narrow;
}
