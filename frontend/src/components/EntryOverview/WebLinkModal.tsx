import React, { useState } from 'react';
import { toast } from 'sonner';

import { BASE_URL } from '@/utils/config';
import Button from '../Buttons/Button';
import ModalCancelButton from '@/components/Buttons/ModalCancelButton'

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

  // Saving link
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

        {/* Show mode */}
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
              <p className="text-gray-500 italic">No link yet.</p>
            )}

            <div className="flex justify-end mt-6">

              {/* Close button */}
              <ModalCancelButton onClose={() => setLinkForId(null)} />

              {/* Edit button */}
              <Button text="Edit" onClick={() => setEditingLink(true)} />

            </div>
          </>
        ) : (
          <>
            {/* Edit mode */}
            <input
              value={webLink}
              onChange={(e) => setWebLink(e.target.value)}
              placeholder="https://example.com"
              className="w-full p-2 border rounded text-sm"
            />

            <div className="flex justify-end space-x-4 mt-4">

              {/* Cancel button */}
              <ModalCancelButton
                onClose={() => {
                  setLinkForId(null);
                  setWebLink(currentLink);
                }}
              />

              {/* Save button */}
              <Button
                text={saving ? 'Saving...' : 'Save'}
                type="submit"
                isDisabled={saving}
                onClick={handleSave}
              />

            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default WebLinkModal;