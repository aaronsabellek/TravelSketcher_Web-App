import { useEffect, useState } from 'react';

interface UseEntryFormStateProps {
  type: 'destination' | 'activity';
  initialData?: {
    title?: string;
    country?: string;
    status?: 'planned' | 'done';
    tags?: string[];
    img_link?: string;
  };
  onSubmit: (data: any) => Promise<void>;
}

// Hooks for EntryForm
export function useEntryFormState({ type, initialData, onSubmit }: UseEntryFormStateProps) {

  const [title, setTitle] = useState('');
  const [country, setCountry] = useState('');
  const [status, setStatus] = useState<'planned' | 'done'>('planned');
  const [tagInput, setTagInput] = useState('');
  const [tagsArray, setTagsArray] = useState<string[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [selectedImageUrl, setSelectedImageUrl] = useState('');

  // Remove tags
  const removeTag = (tagToRemove: string) => {
    setTagsArray((prevTags) => prevTags.filter((tag) => tag !== tagToRemove));
  };

  // Submit
  const handleFormSubmit = async (e: React.FormEvent) => {

    e.preventDefault();
    if (!title.trim()) return;

    setIsSaving(true);

    const formData = {
      title,
      country,
      img_link: selectedImageUrl,
      status,
      tags: tagsArray,
    };

    await onSubmit(formData);
    setIsSaving(false);
  };

  // Load initial data in edit mode
  useEffect(() => {
    if (!initialData) return;
    const { title, country, status, tags, img_link } = initialData;
    if (title) setTitle(title);
    if (country) setCountry(country);
    if (status) setStatus(status);
    if (tags) setTagsArray(tags);
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
    isSaving,
    removeTag,
    handleFormSubmit,
  };
}