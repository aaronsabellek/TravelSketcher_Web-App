import React from 'react';

interface DeleteConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  deleting: boolean;
  itemType: 'destination' | 'activity' | 'user';
}

const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  isOpen,
  onClose,
  onDelete,
  deleting,
  itemType
}) => {
  if (!isOpen) return null;

  const getWarningText = () => {
    switch (itemType) {
      case 'destination':
        return 'Bist du sicher, dass du diese Destination löschen möchtest? Dies kann nicht rückgängig gemacht werden.';
      case 'activity':
        return 'Bist du sicher, dass du diese Activity löschen möchtest? Dies kann nicht rückgängig gemacht werden.';
      case 'user':
        return 'Bist du sicher, dass du deinen Account löschen möchtest? Alle Daten werden dauerhaft entfernt.';
      default:
        return 'Bist du sicher, dass du dieses Element löschen möchtest?';
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-80">
        <h2 className="text-lg font-semibold mb-4">{itemType} löschen?</h2>
        <p className="mb-4 text-sm text-gray-600">
          {getWarningText()}
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