import React, { useState } from 'react';
import { toast } from 'sonner';

import { BASE_URL } from '@/utils/config';
import Button from '../Buttons/Button';
import ModalCancelButton from '@/components/Buttons/ModalCancelButton'

interface NoteModalProps<T> {
  type: 'destination' | 'activity';
  noteText: string;
  setNoteText: (text: string) => void;
  editingNote: boolean;
  setEditingNote: (edit: boolean) => void;
  noteForId: string | null;
  setNoteForId: (id: string | null) => void;
  saveNote: () => void;
  items: T[];
  setItems: React.Dispatch<React.SetStateAction<T[]>>;
  textField?: string;
}

// Administers note of an entry
const NoteModal = <T extends { id: string; free_text?: string }>({
  type,
  noteText,
  setNoteText,
  editingNote,
  setEditingNote,
  noteForId,
  setNoteForId,
  items,
  setItems,
}: NoteModalProps<T>) => {

  const [savingNote, setSavingNote] = useState(false);

  if (!noteForId) return null;

  // Save note
  const handleSaveNote = async () => {
    if (!noteForId) return;

    setSavingNote(true);
    try {
      const response = await fetch(`${BASE_URL}/${type}/edit_notes/${noteForId}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ free_text: noteText }),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(data.error || 'Error saving.');
        return
      }

      setItems((prev) =>
        prev.map((d) =>
          d.id === noteForId ? { ...d, free_text: noteText } : d
        )
      );

      toast.success('Note saved!');
      setEditingNote(false);
    } catch (err) {
      console.error(err);
      toast.error('Save failed.');
    } finally {
      setSavingNote(false);
    }
  };

  // Get note
  const currentNote = items.find((d) => d.id === noteForId)?.free_text || '';

  return (
    <div data-ignore-click className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-[90%] max-w-md relative">
        <h2 className="text-lg font-semibold mb-4">Notes for {type}</h2>

        {/* Show mode */}
        {!editingNote ? (
          <>
            <div className="whitespace-pre-wrap text-sm text-gray-800 overflow-y-auto max-h-64">

            {/* If there is no note yet */}
            {noteText.trim() === '' ? (
              <p className="text-gray-500 italic">No note yet.</p>
            ) : (
              // Note: URLs as links
              noteText
                .split(/(\s+)/)
                .map((part, i) =>
                  part.match(/^https?:\/\/\S+$/) ? (
                    <a
                      key={i}
                      href={part}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline break-all"
                    >
                      {part}
                    </a>
                  ) : (
                    part
                  )
                )
              )}

            </div>

            <div className="flex justify-end mt-6">

              {/* Close button */}
              <ModalCancelButton onClose={() => setNoteForId(null)} />

              {/* Edit button */}
              <Button text="Edit" onClick={() => setEditingNote(true)} />
            </div>
          </>
        ) : (
          <>
            {/* Edit mode */}
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              maxLength={1000}
              rows={8}
              className="w-full p-2 border rounded resize-none whitespace-pre-wrap break-words text-sm"
            />

            {/* Show characters */}
            <div className="text-right text-sm text-gray-500 mt-1">
              {noteText.length}/1000 characters
            </div>

            <div className="flex justify-end space-x-4 mt-4">

              {/* Cancel button */}
              <ModalCancelButton
                onClose={() => {
                  setNoteForId(null);
                  setNoteText(currentNote);
                }}
              />

              {/* Save button */}
              <Button
                text={savingNote ? 'Saving...' : 'Save'}
                type="submit"
                isDisabled={savingNote}
                onClick={handleSaveNote}
              />

            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default NoteModal;