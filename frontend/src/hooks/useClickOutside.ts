import { useEffect } from 'react';

// Close element when user clicks outside
export const useClickOutside = (
  refs: React.RefObject<HTMLElement | null>[],
  handler: () => void,
  active: boolean = true
  ) => {
  useEffect(() => {
    const listener = (e: MouseEvent) => {

      const clickedInsideAny = refs.some(
        ref => ref.current && ref.current.contains(e.target as Node)
      );
      if (clickedInsideAny) return;
      handler();
    };

    if (!active) return;

    document.addEventListener('mousedown', listener, { passive: true });
    return () => {
      document.removeEventListener('mousedown', listener);
    };
  }, [refs, handler, active]);
};