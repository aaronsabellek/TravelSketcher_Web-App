import React from 'react';

import ModalCancelButton from '../Buttons/ModalCancelButton';
import Button from '../Buttons/Button';

interface DeleteConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
  deleting: boolean;
  itemType: 'destination' | 'activity' | 'user';
}

// Confirmation window for deletion of element
const DeleteConfirmModal: React.FC<DeleteConfirmModalProps> = ({
  isOpen,
  onClose,
  onDelete,
  deleting,
  itemType
}) => {

  // Cancel if window is closed
  if (!isOpen) return null;

  // Warning texts
  const getWarningText = () => {
    switch (itemType) {
      case 'destination':
        return 'Are you sure you want to delete this destination? This cannot be undone.';
      case 'activity':
        return 'Are you sure you want to delete this activity? This cannot be undone.';
      case 'user':
        return 'Are you sure you want to delete your account? All data will be permanently deleted.';
      default:
        return 'Are you sure you want to delete this item?';
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-80">

        {/* Warning Text */}
        <h2 className="text-lg font-semibold mb-4">Delete {itemType}?</h2>
        <p className="mb-4 text-sm text-gray-600">
          {getWarningText()}
        </p>

        <div className="flex justify-end space-x-4">

          {/* Cancel button */}
          <ModalCancelButton onClose={onClose} />

          {/* Delete Button */}
          <Button
            text={deleting ? 'Deleting...' : 'Delete'}
            isDisabled={deleting} // Button is disabled while deleting
            onClick={onDelete} // onClick triggers the deletion
          />

        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;