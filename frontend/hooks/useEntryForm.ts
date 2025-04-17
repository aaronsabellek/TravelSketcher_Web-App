import { useState, useEffect, useRef } from 'react';
import { FormData } from '../src/formData';
import BASE_URL from '../utils/config';
import selectedImageUrl from '../components/EntryForm/ImageSearchModal'

interface UseEntryFormProps {
  onSubmit: (data: any) => void;
  initialData?: {
    title?: string;
    country?: string;
    status?: 'planned' | 'done';
    tags?: string[];
    imageUrl?: string;
  };
}

export const useEntryForm = ({ onSubmit }: UseEntryFormProps) => {
  const [title, setTitle] = useState('');
  const [country, setCountry] = useState('');
  const [status, setStatus] = useState<'planned' | 'done'>('planned');
  const [tagInput, setTagInput] = useState('');
  const [tagsArray, setTagsArray] = useState<string[]>([]);
  const [isSaving, setIsSaving] = useState(false);

  const [selectedImageUrl, setSelectedImageUrl] = useState('');

  const removeTag = (tagToRemove: string) => {
    setTagsArray((prevTags) => {
      const updated = prevTags.filter((tag) => tag !== tagToRemove);
      return updated;
    });
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    setIsSaving(true);

    const formData = {
      title,
      country,
      img_link: selectedImageUrl,
      status,
      tags: tagsArray.join(','),
    };

    await onSubmit(formData);
    setIsSaving(false);
  };

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
    removeTag,
    isSaving,
    handleFormSubmit,
    selectedImageUrl,
    setSelectedImageUrl,
  };
};