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

  const formattedInitialData = initialData
  ? {
      ...initialData,
      tags: initialData.tags ? initialData.tags.split(',').map(tag => tag.trim()) : [], // tags als Array
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