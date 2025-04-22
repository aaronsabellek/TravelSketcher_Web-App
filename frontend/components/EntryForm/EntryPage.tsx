import { useState, useEffect } from 'react';
import EntryForm from '../../components/EntryForm';
import { useRouter } from 'next/router';
import Container from '../../components/Container';
import { toast } from 'sonner';
import { BASE_URL } from '../../utils/config';

interface EntryPageProps {
  mode: 'add' | 'edit';
  type: 'destination' | 'activity';
}

const EntryPage: React.FC<EntryPageProps> = ({ mode, type }) => {
  const router = useRouter();

  // IDs sicher und getrennt behandeln
  const rawId = router.query.id as string | undefined;
  const [destinationId, setDestinationId] = useState<string | null>(null);

  // formData type
  type EntryFormData = {
    title?: string;
    country?: string;
    tags?: string[];
    img_link?: string;
    destination_id?: string;
  };

  const [initialData, setInitialData] = useState<EntryFormData | null>(null);

  useEffect(() => {
    if (!router.isReady || !rawId) return;

    let endpoint = '';

    if (mode === 'edit') {
      endpoint = `${BASE_URL}/${type}/get/${rawId}`;

      fetch(endpoint, {
        credentials: 'include',
      })
        .then((res) => res.json())
        .then((data) => {
          const itemData = data[type];
          if (typeof itemData.tags === 'string') {
            itemData.tags = itemData.tags
              .split(',')
              .map((tag: string) => tag.trim())
              .filter((tag: string) => tag.length > 0);
          }

          setInitialData(itemData);

          // destination_id separat merken, falls Activity editiert wird
          if (type === 'activity' && itemData.destination_id) {
            setDestinationId(itemData.destination_id);
          }
        })
        .catch((err) => {
          console.error(err);
          toast.error('Fehler beim Laden.');
        });
    } else if (mode === 'add' && type === 'activity') {
      // Hier ist rawId = destination_id (weil aus URL: /activity/add/[id])
      setDestinationId(rawId);
    }

  }, [router.isReady, mode, rawId, type]);

  const handleSubmit = async (formData: EntryFormData) => {
    if (!router.isReady) {
      toast.error('Router ist noch nicht bereit.');
      return;
    }

    let endpoint = '';

    if (mode === 'add' && type === 'destination') {
      endpoint = `${BASE_URL}/destination/add`;
    } else if (mode === 'add' && type === 'activity') {
      if (!destinationId) {
        toast.error('Destination ID fehlt.');
        return;
      }
      endpoint = `${BASE_URL}/activity/add/${destinationId}`;
    } else if (mode === 'edit') {
      if (!rawId) {
        toast.error('ID fehlt.');
        return;
      }
      endpoint = `${BASE_URL}/${type}/edit/${rawId}`;
    } else {
      toast.error('Unbekannter Modus oder Typ.');
      return;
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern');

      toast.success(mode === 'add' ? 'Erfolgreich hinzugefügt!' : 'Erfolgreich aktualisiert!');

      // Nach dem Speichern weiterleiten
      const pushRoute =
        type === 'destination'
          ? `/destination/get_all`
          : `/activity/get_all/${destinationId}`;
      router.push(pushRoute);

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