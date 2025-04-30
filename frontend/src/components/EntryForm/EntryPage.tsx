import EntryForm from '.';
import Container from '@/components/Container';
import { useEntryFormHandler } from '@/hooks/useEntryFormHandler';

interface EntryPageProps {
  mode: 'add' | 'edit';
  type: 'destination' | 'activity';
}

// Formular to add or edit an entry
const EntryPage: React.FC<EntryPageProps> = ({ mode, type }) => {

  const { initialData, handleSubmit } = useEntryFormHandler(mode, type);

  // Check if tags are a string or already an array
  const formattedInitialData = initialData
  ? {
      ...initialData,
      tags:
        Array.isArray(initialData.tags)
          ? initialData.tags
          : typeof initialData.tags === 'string'
            ? initialData.tags.split(',').map((tag) => tag.trim())
            : [],
    }
  : undefined;

  return (
    <Container title={mode === 'add' ? `Add ${type}` : `Edit ${type}`}>
      <EntryForm
        type={type}
        onSubmit={handleSubmit}
        initialData={formattedInitialData}
        submitLabel={mode === 'add' ? `Add ${type}` : `Edit ${type}`}
      />
    </Container>
  );
};

export default EntryPage;