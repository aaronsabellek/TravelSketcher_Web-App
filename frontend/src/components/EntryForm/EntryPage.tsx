import EntryForm from '.';
import Container from '../Container';
import { useEntryFormHandler } from '../../hooks/useEntryFormHandler';


interface EntryPageProps {
  mode: 'add' | 'edit';
  type: 'destination' | 'activity';
}

const EntryPage: React.FC<EntryPageProps> = ({ mode, type }) => {
  const { initialData, handleSubmit } = useEntryFormHandler(mode, type);

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