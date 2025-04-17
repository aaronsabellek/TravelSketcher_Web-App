import { useEffect } from 'react';
import { FormData } from '../../src/formData';
import EntryForm from '../../components/EntryForm';
import { useRouter } from 'next/router';
import Container from '../../components/Container';
import { toast } from 'sonner';
import BASE_URL from '../../utils/config';

const AddPage = () => {
  const router = useRouter();

  const handleSubmit = async (formData: FormData) => {
    try {
      const response = await fetch(`${BASE_URL}/destination/add`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern');
      toast.success('Erfolgreich gespeichert!');
      router.push('/destination/get_all');
    } catch (err) {
      console.error(err);
      toast.error('Fehler beim Speichern.');
    }
  };

  return (
    <Container title="Add destination">
        <EntryForm
            onSubmit={handleSubmit}
            submitLabel="Destination speichern"
        />
    </Container>
  );
};

export default AddPage;