import { useState, useMemo } from "react";
import { Destination, Activity } from "../types/models";
import { toast } from "sonner";
import { BASE_URL } from '../utils/config';

export const useReorder = <T extends Destination | Activity>(
  items: T[],
  setItems: (items: T[]) => void
) => {
  const [isReorderMode, setIsReorderMode] = useState(false);
  const [originalOrder, setOriginalOrder] = useState<T[]>([]);
  const [savedOrder, setSavedOrder] = useState<T[] | null>(null);

  const moveDestinationUp = (index: number) => {
    if (index === 0) return;
    const newDestinations = [...items];
    [newDestinations[index - 1], newDestinations[index]] = [newDestinations[index], newDestinations[index - 1]];
    setItems(newDestinations);
  };

  const moveDestinationDown = (index: number) => {
    if (index === items.length - 1) return;
    const newDestinations = [...items];
    [newDestinations[index + 1], newDestinations[index]] = [newDestinations[index], newDestinations[index + 1]];
    setItems(newDestinations);
  };

  const isSameOrder = (a: T[], b: T[]) =>
    a.length === b.length && a.every((dest, idx) => dest.id === b[idx].id);

  const hasOrderChanged = useMemo(() => !isSameOrder(items, originalOrder), [items, originalOrder]);

  const toggleReorderMode = () => {
    if (!isReorderMode) {
      setOriginalOrder([...items]);
      setIsReorderMode(true);
    } else {
      setItems(savedOrder ? [...savedOrder] : [...originalOrder]);
      setIsReorderMode(false);
    }
  };

  const saveNewOrder = async () => {
    try {
      const orderedIds = items.map(dest => dest.id);
      const response = await fetch(`${BASE_URL}/destination/reorder`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_order: orderedIds }),
      });

      if (!response.ok) throw new Error("Fehler beim Speichern der Reihenfolge");

      toast.success("Reihenfolge erfolgreich gespeichert!");
      setSavedOrder([...items]);
    } catch (err) {
      console.error("Fehler beim Speichern:", err);
      toast.error("Beim Speichern ist ein Fehler aufgetreten.");
    }
  };

  return {
    isReorderMode,
    toggleReorderMode,
    moveDestinationUp,
    moveDestinationDown,
    saveNewOrder,
    hasOrderChanged,
  };
};