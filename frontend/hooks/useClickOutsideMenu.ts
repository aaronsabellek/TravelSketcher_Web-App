import { useEffect } from "react";

export function useClickOutsideMenu(
  menuRef: React.RefObject<HTMLElement | null>,
  isMenuOpen: boolean,
  closeMenu: () => void
) {
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        closeMenu(); // Menü schließen
      }
    };

    if (isMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isMenuOpen, menuRef, closeMenu]);
}