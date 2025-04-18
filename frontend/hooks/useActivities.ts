import { useEffect, useState } from 'react';
import { Activity } from '../types/models';
import { BASE_URL } from '../utils/config';

export const useActivities = () => {
  const [activities, setActivities] = useState<Activity[]>([]);

  return {
    items: activities,
    setItems: setActivities,
  };
};