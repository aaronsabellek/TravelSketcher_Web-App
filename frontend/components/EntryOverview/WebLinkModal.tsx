import React, { useState } from 'react';
import { BASE_URL } from '../../utils/config';
import { toast } from 'sonner';

interface WebLinkModalProps<T> {
  items: T[];
  setItems: React.Dispatch<React.SetStateAction<T[]>>;
  webLink: string;
  setWebLink: (link: string) => void;
  editingLink: boolean;
  setEditingLink: (val: boolean) => void;
  linkForId: string | null;
  setLinkForId: (id: string | null) => void;
}

const WebLinkModal = <T extends { id: string; web_link?: string }>({
  items,
  setItems,
  webLink,
  setWebLink,
  editingLink,
  setEditingLink,
  linkForId,
  setLinkForId,
}: WebLinkModalProps<T>) => {
  if (!linkForId) return null;

  const currentLink = items.find((i) => i.id === linkForId)?.web_link || '';
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    if (!linkForId) return;

    setSaving(true);
    try {
      const res = await fetch(`${BASE_URL}/activity/edit_link/${linkForId}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ web_link: webLink }),
      });

      if (!res.ok) throw new Error('Fehler beim Speichern');

      setItems((prev) =>
        prev.map((i) =>
          i.id === linkForId ? { ...i, web_link: webLink } : i
        )
      );

      toast.success('Link gespeichert!');
      setEditingLink(false);
    } catch (err) {
      console.error(err);
      toast.error('Fehler beim Speichern');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/30 z-50" data-ignore-click>
      <div className="bg-white p-6 rounded-lg shadow-xl w-[90%] max-w-md relative">
        <h2 className="text-lg font-semibold mb-4">Web-Link zur Aktivität</h2>

        {!editingLink ? (
          <>
            {currentLink ? (
              <a
                href={currentLink}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline break-all"
              >
                {currentLink}
              </a>
            ) : (
              <p className="text-gray-500 italic">Kein Link vorhanden.</p>
            )}
            <button
              onClick={() => setEditingLink(true)}
              className="absolute top-4 right-4 text-sm text-blue-600 hover:underline"
            >
              ✏️ Bearbeiten
            </button>
            <div className="flex justify-end mt-6">
              <button
                className="px-4 py-2 text-gray-600 hover:text-black"
                onClick={() => setLinkForId(null)}
              >
                Schließen
              </button>
            </div>
          </>
        ) : (
          <>
            <input
              value={webLink}
              onChange={(e) => setWebLink(e.target.value)}
              placeholder="https://example.com"
              className="w-full p-2 border rounded text-sm"
            />
            <div className="flex justify-end space-x-4 mt-4">
              <button
                className="px-4 py-2 text-gray-600 hover:text-black"
                onClick={() => {
                  setEditingLink(false);
                  setWebLink(currentLink);
                }}
              >
                Abbrechen
              </button>
              <button
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? 'Speichern...' : 'Speichern'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default WebLinkModal;