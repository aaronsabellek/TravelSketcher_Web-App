import React, { useState } from 'react';
import { Destination } from '../types/models';
import { toast } from "sonner";
import { BASE_URL } from '../utils/config';

interface NoteModalProps<T> {
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

const NoteModal = <T extends { id: string; free_text?: string }>({
  noteText,
  setNoteText,
  editingNote,
  setEditingNote,
  noteForId,
  setNoteForId,
  items,
  setItems,
  textField = 'free_text',
}: NoteModalProps<T>) => {
  if (!noteForId) return null;

  const [savingNote, setSavingNote] = useState(false);

  const handleSaveNote = async () => {
    if (!noteForId) return;

    setSavingNote(true);
    try {
      const response = await fetch(`${BASE_URL}/destination/edit_notes/${noteForId}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ free_text: noteText }),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern der Notiz');

      setItems((prev) =>
        prev.map((d) =>
          d.id === noteForId ? { ...d, free_text: noteText } : d
        )
      );

      toast.success('Notiz gespeichert!');
      setEditingNote(false);
    } catch (err) {
      console.error(err);
      toast.error('Speichern fehlgeschlagen.');
    } finally {
      setSavingNote(false);
    }
  };

  const currentNote = items.find((d) => d.id === noteForId)?.free_text || '';

  return (
    <div data-ignore-click className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-[90%] max-w-md relative">
        <h2 className="text-lg font-semibold mb-4">Notizen zur Destination</h2>

        {!editingNote ? (
          <>
            <div className="whitespace-pre-wrap text-sm text-gray-800 overflow-y-auto max-h-64">
              {noteText
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
                )}
            </div>
            <button
              onClick={() => setEditingNote(true)}
              className="absolute top-4 right-4 text-sm text-blue-600 hover:underline"
            >
              ✏️ Bearbeiten
            </button>
            <div className="flex justify-end mt-6">
              <button
                className="px-4 py-2 text-gray-600 hover:text-black"
                onClick={() => setNoteForId(null)}
              >
                Schließen
              </button>
            </div>
          </>
        ) : (
          <>
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              maxLength={1000}
              rows={8}
              className="w-full p-2 border rounded resize-none whitespace-pre-wrap break-words text-sm"
            />
            <div className="text-right text-sm text-gray-500 mt-1">
              {noteText.length}/1000 Zeichen
            </div>
            <div className="flex justify-end space-x-4 mt-4">
              <button
                className="px-4 py-2 text-gray-600 hover:text-black"
                onClick={() => {
                  setEditingNote(false);
                  setNoteText(currentNote);
                }}
              >
                Abbrechen
              </button>
              <button
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                onClick={handleSaveNote}
                disabled={savingNote}
              >
                {savingNote ? 'Speichere...' : 'Speichern'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default NoteModal;