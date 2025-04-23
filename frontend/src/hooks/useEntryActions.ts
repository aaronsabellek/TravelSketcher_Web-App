import { useRouter } from 'next/router';
import { useRef, useEffect, useState } from 'react';
import { BASE_URL } from '../utils/config';
import { Destination, Activity } from '../types/models';

type Item = Destination | Activity;

export function useEntryActions<T extends Item>(
  items: T[],
  setItems: React.Dispatch<React.SetStateAction<T[]>>,
  routeBase: string,
) {

  const router = useRouter();

  // Menu open/close
  const [menuOpenFor, setMenuOpenFor] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpenFor(null);
      }
    };

    if (menuOpenFor) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuOpenFor]);

  // Edit
  const handleEdit = (id: string) => {
    router.push(`${routeBase}/edit/${id}`);
  };

  // Delete confirm
  const [confirmDeleteId, setConfirmDeleteId] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  const handleDeleteConfirm = (id: string) => {
    setMenuOpenFor(null);
    setConfirmDeleteId(id);
  };

  // Notes
  const [noteForId, setNoteForId] = useState<string | null>(null);
  const [noteText, setNoteText] = useState('');
  const [editingNote, setEditingNote] = useState(false);
  const [savingNote, setSavingNote] = useState(false);

  const openNote = (id: string) => {
    const item = items.find((d) => d.id === id);
    setNoteText(item?.free_text || '');
    setNoteForId(id);
    setEditingNote(false);
  };

  const saveNote = async () => {
    if (!noteForId) return;
    if (noteText.length > 1000) {
      alert('Die Notiz darf maximal 1000 Zeichen lang sein.');
      return;
    }

    setSavingNote(true);

    try {
      const response = await fetch(`${BASE_URL}/${routeBase}/edit_notes/${noteForId}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ free_text: noteText }),
      });

      if (!response.ok) throw new Error('Speichern fehlgeschlagen');

      setItems((prev) =>
        prev.map((d) => (d.id === noteForId ? { ...d, free_text: noteText } : d))
      );
      setNoteForId(null);
    } catch (err) {
      alert('Fehler beim Speichern der Notiz.');
    } finally {
      setSavingNote(false);
    }
  };


  return {
    menuOpenFor,
    setMenuOpenFor,
    menuRef,
    handleEdit,
    handleDeleteConfirm,
    confirmDeleteId,
    setConfirmDeleteId,
    deleting,
    setDeleting,
    noteForId,
    setNoteForId,
    noteText,
    setNoteText,
    editingNote,
    setEditingNote,
    openNote,
    saveNote,
  };
}