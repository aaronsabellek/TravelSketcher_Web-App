import { useEffect } from 'react';

export const useClickOutside = (
  ref: React.RefObject<HTMLDivElement | null>,
  handler: () => void,
  active: boolean = true
) => {
  useEffect(() => {
    const listener = (e: MouseEvent) => {
      if (!ref.current || ref.current.contains(e.target as Node)) return;
      handler();
    };

    if (!active) return;

    document.addEventListener('mousedown', listener, { passive: true });
    return () => {
      document.removeEventListener('mousedown', listener);
    };
  }, [ref, handler, active]);
};