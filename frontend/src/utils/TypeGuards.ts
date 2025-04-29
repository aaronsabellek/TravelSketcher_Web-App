import { Destination, Activity } from '@/types/models';

export function isActivity(entry: Destination | Activity): entry is Activity {
    return (entry as Activity).web_link !== undefined;
}

export function isDestination(entry: Destination | Activity): entry is Destination {
    return 'country' in entry;
  }