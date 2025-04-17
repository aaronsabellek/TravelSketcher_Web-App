import { useEffect } from 'react';

export function useFormSync({
  form,
  selectedImageUrl,
  updateTitle,
}: {
  form: any;
  selectedImageUrl: string | null;
  updateTitle: (title: string) => void;
}) {

  // Titel synchronisieren
  useEffect(() => {
    if (form.title) {
      updateTitle(form.title);
    }
  }, [form.title, updateTitle]);

  // Bild synchronisieren
  useEffect(() => {
    if (selectedImageUrl) {
      form.setSelectedImageUrl(selectedImageUrl);
    }
  }, [selectedImageUrl, form]);
}