import { useEffect, useState } from 'react';

interface UseEntryFormStateProps {
  initialData?: {
    title?: string;
    country?: string;
    status?: 'planned' | 'done';
    tags?: string | string[];
    img_link?: string;
  };
}

// Hooks for EntryForm
export function useEntryFormState({ initialData }: UseEntryFormStateProps) {

  const [title, setTitle] = useState('');
  const [country, setCountry] = useState('');
  const [status, setStatus] = useState<'planned' | 'done'>('planned');
  const [tagInput, setTagInput] = useState('');
  const [tagsArray, setTagsArray] = useState<string[]>([]);
  const [selectedImageUrl, setSelectedImageUrl] = useState('');

  // Remove tags
  const removeTag = (tagToRemove: string) => {
    setTagsArray((prevTags) => prevTags.filter((tag) => tag !== tagToRemove));
  };

  // Load initial data in edit mode
  useEffect(() => {
    if (!initialData) return;
    const { title, country, status, tags, img_link } = initialData;
    if (title) setTitle(title);
    if (country) setCountry(country);
    if (status) setStatus(status);

    if (tags) {
      setTagsArray(typeof tags === 'string' ? tags.split(',').map((tag) => tag.trim()) : tags);
    }

    if (img_link) setSelectedImageUrl(img_link);
  }, [initialData]);

  return {
    title,
    setTitle,
    country,
    setCountry,
    status,
    setStatus,
    tagInput,
    setTagInput,
    tagsArray,
    setTagsArray,
    selectedImageUrl,
    setSelectedImageUrl,
    removeTag,
  };
}