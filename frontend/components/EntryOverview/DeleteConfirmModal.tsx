import React from 'react';

interface DeleteConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  deleting: boolean;
}

const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  isOpen,
  onClose,
  onDelete,
  deleting,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-80">
        <h2 className="text-lg font-semibold mb-4">Destination löschen?</h2>
        <p className="mb-4 text-sm text-gray-600">
          Bist du sicher, dass du diese Destination löschen möchtest? Dies kann nicht rückgängig gemacht werden.
        </p>
        <div className="flex justify-end space-x-4">
          <button
            className="px-4 py-2 text-gray-600 hover:text-black"
            onClick={onClose}
          >
            Abbrechen
          </button>
          <button
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            onClick={onDelete}
            disabled={deleting}
          >
            {deleting ? 'Lösche...' : 'Ja, löschen'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;