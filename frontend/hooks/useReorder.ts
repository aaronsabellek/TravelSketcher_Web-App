import { useState, useMemo } from "react";
import { Destination, Activity } from "../types/models";
import { toast } from "sonner";
import { BASE_URL } from '../utils/config';

export const useReorder = <T extends Destination | Activity>(
  type: 'destination'| 'activity',
  items: T[],
  setItems: (items: T[]) => void
) => {
  const [isReorderMode, setIsReorderMode] = useState(false);
  const [originalOrder, setOriginalOrder] = useState<T[]>([]);
  const [savedOrder, setSavedOrder] = useState<T[] | null>(null);

  const moveDestinationUp = (index: number) => {
    if (index === 0) return;
    const newItems = [...items];
    [newItems[index - 1], newItems[index]] = [newItems[index], newItems[index - 1]];
    setItems(newItems);
  };

  const moveDestinationDown = (index: number) => {
    if (index === items.length - 1) return;
    const newItems = [...items];
    [newItems[index + 1], newItems[index]] = [newItems[index], newItems[index + 1]];
    setItems(newItems);
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
      const orderedIds = items.map(item => item.id);

      let endpoint = `${BASE_URL}/${type}/reorder`;

      if (type === 'activity') {
        const firstActivity = items[0] as Activity;
        const activityDestinationId = firstActivity?.destination_id;
        if (!activityDestinationId) {
          throw new Error("Keine destination_id bei activity gefunden.");
        }
        endpoint = `${BASE_URL}/activity/reorder/${activityDestinationId}`;
      }

      const response = await fetch(endpoint, {
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