import { useState, useMemo } from 'react';
import { toast } from 'sonner';

import { Destination, Activity } from '@/types/models';
import { BASE_URL } from '@/utils/config';

// Reorder entries
export const useReorder = <T extends Destination | Activity>(
  type: 'destination'| 'activity',
  items: T[],
  setItems: (items: T[]) => void
) => {

  const [isReorderMode, setIsReorderMode] = useState(false);
  const [originalOrder, setOriginalOrder] = useState<T[]>([]);
  const [savedOrder, setSavedOrder] = useState<T[] | null>(null);

  // Move entry
  const moveEntry = (index: number, direction: 'up' | 'down') => {
    const newItems = [...items];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;

    // Check for valid index
    if (targetIndex < 0 || targetIndex >= items.length) return;

    // Swap entries
    [newItems[index], newItems[targetIndex]] = [newItems[targetIndex], newItems[index]];
    setItems(newItems);
  };

  // Check for same order
  const isSameOrder = (a: T[], b: T[]) =>
    a.length === b.length && a.every((dest, idx) => dest.id === b[idx].id);

  // Check if order has changed
  const hasOrderChanged = useMemo(() => !isSameOrder(items, originalOrder), [items, originalOrder]);

  // Toggle reorder mode
  const toggleReorderMode = () => {
    if (!isReorderMode) {
      setOriginalOrder([...items]);
      setIsReorderMode(true);
    } else {
      setItems(savedOrder ? [...savedOrder] : [...originalOrder]);
      setIsReorderMode(false);
    }
  };

  // Save new order
  const saveNewOrder = async () => {
    try {
      const orderedIds = items.map(item => item.id);

      let endpoint = `${BASE_URL}/${type}/reorder`;

      if (type === 'activity') {
        const firstActivity = items[0] as Activity;
        const activityDestinationId = firstActivity?.destination_id;
        if (!activityDestinationId) {
          throw new Error('No destination_id found for activity.');
        }
        endpoint = `${BASE_URL}/activity/reorder/${activityDestinationId}`;
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_order: orderedIds }),
      });

      if (!response.ok) throw new Error('Error saving the order');

      toast.success('Order saved successfully!');
      setSavedOrder([...items]);
    } catch (err) {
      console.error('Error saving:', err);
      toast.error('An error occurred while saving.');
    }
  };

  return {
    isReorderMode,
    toggleReorderMode,
    moveEntry,
    saveNewOrder,
    hasOrderChanged,
  };
};