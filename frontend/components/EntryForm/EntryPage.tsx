import { useState, useEffect } from 'react';
import { FormData } from '../../src/formData';
import EntryForm from '../../components/EntryForm';
import { useRouter } from 'next/router';
import Container from '../../components/Container';
import { toast } from 'sonner';
import BASE_URL from '../../utils/config';

interface EntryPageProps {
    mode: 'add' | 'edit';
    type: 'destination' | 'activity';
  }

  const EntryPage: React.FC<EntryPageProps> = ({ mode, type }) => {
    const router = useRouter();
    const { id } = router.query;

    type EntryFormData = {
        title?: string;
        country?: string;
        status?: 'planned' | 'done';
        tags?: string[];
        img_link?: string;
      };
    const [initialData, setInitialData] = useState<EntryFormData | null>(null);

    useEffect(() => {
      if (!router.isReady) return;

      if (mode === 'edit' && id) {
        fetch(`${BASE_URL}/${type}/get/${id}`, {
          credentials: 'include',
        })
          .then((res) => res.json())
          .then((data) => {
            const destinationData = data.destination; // Extrahiere das 'destination' Objekt
            if (typeof destinationData.tags === 'string') {
                destinationData.tags = destinationData.tags
                    .split(',')
                    .map((tag: string) => tag.trim())
                    .filter((tag: string) => tag.length > 0);
            }
            setInitialData(destinationData); // Setze die Daten in den State
          })
          .catch((err) => console.error(err));
      }
    }, [router.isReady, mode, id, type]);


    const handleSubmit = async (formData: FormData) => {
      try {
        const endpoint =
          mode === 'add'
            ? `${BASE_URL}/${type}/add`
            : `${BASE_URL}/${type}/edit/${id}`;

        const response = await fetch(endpoint, {
          method: mode === 'add' ? 'POST' : 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });

        if (!response.ok) throw new Error('Fehler beim Speichern');

        toast.success(
          mode === 'add' ? 'Erfolgreich hinzugefügt!' : 'Erfolgreich aktualisiert!'
        );
        router.push(`/${type}/get_all`);
      } catch (err) {
        console.error(err);
        toast.error('Fehler beim Speichern.');
      }
    };

    return (
      <Container title={mode === 'add' ? `Add ${type}` : `Edit ${type}`}>
        <EntryForm
          type={type}
          onSubmit={handleSubmit}
          initialData={initialData || undefined}
          submitLabel={mode === 'add' ? `Add ${type}` : `Edit ${type}`}
        />
      </Container>
    );
  };

  export default EntryPage;