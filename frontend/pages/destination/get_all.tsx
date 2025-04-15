import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';
import Link from 'next/link';
import BASE_URL from '../../utils/config';

interface Destination {
  id: string;
  img_link: string;
  title: string;
  country: string;
  status: string;
  tags: string;
  duration: string;
  time: string;
  pricing: string;
  travel_duration_flight: string;
  trip_pricing_flight: string;
  free_text: string;
}

const DestinationsPage = () => {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const router = useRouter();

  // Edit/Delete
  const [menuOpenFor, setMenuOpenFor] = useState<string | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<boolean>(false);
  const menuRef = useRef<HTMLDivElement | null>(null);

  // Notes
  const [noteForId, setNoteForId] = useState<string | null>(null);
  const [noteText, setNoteText] = useState<string>('');
  const [editingNote, setEditingNote] = useState<boolean>(false);
  const [savingNote, setSavingNote] = useState<boolean>(false);

  // Reorder
  const [isReorderMode, setIsReorderMode] = useState<boolean>(false);

  // User
  const [userCity, setUserCity] = useState<string | null>(null);

  // Redirect if user is not logged in
  useRedirectIfNotAuthenticated();

  // Funktion zum Abrufen der Destinations
  const fetchDestinations = async () => {
    try {
      const response = await fetch(`${BASE_URL}/destination/get_all`, {
        credentials: 'include',
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Hier könntest du eventuell noch einen Authentifizierungsheader hinzufügen, wenn nötig
          // 'Authorization': `Bearer ${token}`
        },
      });

      if (!response.ok) {
        throw new Error('Fehler beim Laden der Destinations');
      }

      const data = await response.json();
      console.log('API Response:', data); // Antwort loggen

      if (data.destinations) {
        setDestinations(data.destinations);
      }
    } catch (err) {
      console.error('Error fetching destinations:', err);
      setError('Fehler beim Laden der Destinations');
    } finally {
      setLoading(false);
    }
  };

  // Effekt, um die Destinations beim Laden der Seite abzurufen
  useEffect(() => {
    fetchDestinations();
  }, []);

  // Add destination
  const handleAddClick = () => {
    router.push('/destination/add');
  };

  // Get city from user data for Rome2Rio-link
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch(`${BASE_URL}/user/profile`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!res.ok) throw new Error('Fehler beim Abrufen der Userdaten');
        const data = await res.json();
        setUserCity(data.city); // <-- Genau das wollen wir
      } catch (err) {
        console.error('Userdaten konnten nicht geladen werden', err);
      }
    };

    fetchUser();
  }, []);

  // Handler to edit destination
  const handleEdit = (id: string) => {
    // Logik für Bearbeiten
    router.push(`/destination/edit/${id}`);
  };

  // Handler to delete destination
  const handleDeleteConfirm = (id: string) => {
    setMenuOpenFor(null); // Close menu
    setConfirmDeleteId(id); // Open verification window
  };

  // Close edit/delete window with clicks outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpenFor(null); // Menü schließen
      }
    };

    if (menuOpenFor) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [menuOpenFor]);

  // Open notes
  const openNote = (id: string) => {
    const destination = destinations.find((d) => d.id === id);
    setNoteText(destination?.free_text || '');
    setNoteForId(id);
    setEditingNote(false); // Start im Anzeigemodus
  };

  // Save notes
  const saveNote = async () => {
    if (!noteForId) return;
    if (noteText.length > 1000) {
      alert('Die Notiz darf maximal 1000 Zeichen lang sein.');
      return;
    }

    setSavingNote(true);

    try {
      const response = await fetch(`${BASE_URL}/destination/edit_notes/${noteForId}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ free_text: noteText }),
      });

      if (!response.ok) throw new Error('Speichern fehlgeschlagen');

      // Lokale Aktualisierung
      setDestinations((prev) =>
        prev.map((d) => (d.id === noteForId ? { ...d, free_text: noteText } : d))
      );
      setNoteForId(null);
    } catch (err) {
      alert('Fehler beim Speichern der Notiz.');
    } finally {
      setSavingNote(false);
    }
  };

  // Reorder
  const moveDestinationUp = (index: number) => {
    if (index === 0) return;
    const newDestinations = [...destinations];
    [newDestinations[index - 1], newDestinations[index]] = [newDestinations[index], newDestinations[index - 1]];
    setDestinations(newDestinations);
  };

  const moveDestinationDown = (index: number) => {
    if (index === destinations.length - 1) return;
    const newDestinations = [...destinations];
    [newDestinations[index + 1], newDestinations[index]] = [newDestinations[index], newDestinations[index + 1]];
    setDestinations(newDestinations);
  };

  const saveNewOrder = async () => {
    try {
      const orderedIds = destinations.map(dest => dest.id);

      const response = await fetch(`${BASE_URL}/destination/reorder`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_order: orderedIds }),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern der Reihenfolge');
      toast.success('Reihenfolge erfolgreich gespeichert!');
    } catch (err) {
      console.error('Fehler beim Speichern der neuen Reihenfolge:', err);
      toast.error('Beim Speichern ist ein Fehler aufgetreten.');
    }
  };

  return (
    <div className="container max-w-6xl mx-auto px-4">

      {/* Header */}
      <h1 className="text-3xl font-bold mb-2">My Destinations</h1>

      {/* Button zum Aktivieren des Reorder-Modus */}
      <div className="flex justify-between mb-3">
        <button
          onClick={() => setIsReorderMode(!isReorderMode)}
          className={`px-3 py-1 text-xl cursor-pointer transition-all duration-300 ease-in-out transform active:scale-95
            ${isReorderMode ? 'opacity-70' : 'opacity-100'} hover:scale-115`}
        >
          <img src="/change_icon.png" className="h-7" />
        </button>
      </div>

      {/* Loading and Error */}
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {/* Destinations */}
      <div className="grid grid-cols-2 xs:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4">
          {destinations.map((destination, index) => {

            const isExpanded = expandedCard === destination.id;

            {/* Motion für Destination für Animation beim Umsortieren */}
            return (
              <motion.div
                key={destination.id}
                layout="position"
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="relative flex flex-col items-center space-y-2"
              >

                {/* Reorder buttons mit eigener Animation */}
                <AnimatePresence>
                  {isReorderMode && (
                    <motion.div
                      key={`reorder-buttons-${destination.id}`}
                      layout
                      layoutId={`reorder-${destination.id}`}
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.5 }}
                      className="absolute -top-4 z-30 flex space-x-4"
                      data-ignore-click
                    >
                      <button
                        onClick={() => moveDestinationUp(index)}
                        disabled={index === 0}
                        className="transition-transform duration-200 hover:scale-125"
                      >
                        <img src="/left_icon.png" className="h-3" />
                      </button>
                      <button
                        onClick={() => moveDestinationDown(index)}
                        disabled={index === destinations.length - 1}
                        className="transition-transform duration-200 hover:scale-125"
                      >
                        <img src="/right_icon.png" className="h-3" />
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Destination container */}
                <div
                  key={destination.id}
                  className="w-full mt-3 bg-white hover:brightness-95 rounded-lg pb-2"
                  onClick={(e) => {
                    const target = e.target as HTMLElement;
                    if (target.closest('[data-ignore-click]')) return; // Events ignorieren
                    setExpandedCard(isExpanded ? null : destination.id);
                  }}
                >

                  {/* Image */}
                  <div className="relative aspect-[16/12] w-full rounded-lg overflow-hidden">
                    <Link href="/user/profile">
                      <img
                        src='/travel-img-2.png'
                        alt={destination.title}
                        className="w-full h-full object-cover hover:brightness-75 hover:scale-105 transition-all duration-500"
                      />
                    </Link>

                    {/* Edit/Delete/Reorder */}
                    <div className="absolute top-2 right-2 text-white">
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // verhindert, dass das Card-Click-Event ausgelöst wird
                          setMenuOpenFor(destination.id === menuOpenFor ? null : destination.id);
                        }}
                        className="text-xl transition-size duration-300 hover:text-2xl w-7 cursor-pointer"
                      >
                        ⋮
                      </button>

                      {menuOpenFor === destination.id && (
                        <div
                          ref={menuRef}
                          className="absolute right-0 mt-2 w-28 bg-white text-black rounded shadow-md z-50"
                          onClick={(e) => e.stopPropagation()} // damit der Card-Click nicht ausgelöst wird
                        >
                          <button
                            onClick={() => handleEdit(destination.id)}
                            className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                          >
                            ✏️ Edit
                          </button>
                          <button
                            onClick={() => handleDeleteConfirm(destination.id)}
                            className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600"
                          >
                            🗑️ Delete
                          </button>
                        </div>
                      )}

                    </div>
                  </div>

                  {/* Title */}
                  <div>
                    <div className="flex p-2">
                      <div className="mr-5">
                        <Link href="/user/profile">
                          <h2 className="text-xl font-semibold hover:underline">{destination.title}</h2>
                        </Link>
                          <p className="text-sm text-gray-500">{destination.country}</p>
                      </div>
                      <h2 className="mt-2 text-base text-white bg-blue-500 pt-2 px-3 rounded-2xl">{destination.status}</h2>
                    </div>

                    {/* Tags */}
                    <motion.div
                      layout
                      initial={false}
                      animate={{ opacity: 1 }}
                      transition={{ layout: { duration: 0.4, ease: "easeInOut" } }}
                      className="px-2 mt-2"
                    >
                      <div
                        className={
                          isExpanded
                            ? "flex flex-wrap gap-2"
                            : "whitespace-nowrap overflow-x-auto pb-2"
                        }
                      >
                        {destination.tags.split(",").map((tag, idx) => (
                          <motion.span
                            layout
                            key={idx}
                            className="text-xs bg-gray-200 rounded-full px-2 py-1 mr-2 mb-1 inline-block"
                          >
                            {tag.trim()}
                          </motion.span>
                        ))}
                      </div>
                    </motion.div>

                    {/* Link icons */}
                    <div className="flex justify-between space-x-4 p-2">

                      <div className="grid grid-cols-3 gap-3">
                        {userCity && (
                          <button
                          onClick={() =>
                            window.open(`https://www.rome2rio.com/map/${userCity}/${destination.title}`, '_blank')
                          }
                          className="text-blue-500 hover:text-blue-700 cursor-pointer"
                        >
                          <img src="/rome2rio_icon.png" className="h-7 hover:scale-115" />
                        </button>
                        )}

                        <button
                          onClick={() =>
                            window.open(`https://www.booking.com/${destination.title}`, '_blank')
                          }
                          className="text-blue-500 relative right-2 hover:text-blue-700 cursor-pointer"
                        >
                          <img src="/booking_icon.png" className="h-7 hover:scale-115" />
                        </button>

                        <button
                          onClick={() =>
                            window.open(`https://www.google.com/search?q=${destination.title} ${destination.country}`, '_blank')
                          }
                          className="text-blue-500 relative right-2 hover:text-blue-700 cursor-pointer"
                        >
                          <img src="/google_icon.png" className="h-7 hover:scale-115" />
                        </button>

                      </div>

                      {/* Notes icon */}
                      <div>
                        <button
                          data-ignore-click
                          onClick={(e) => {
                            e.stopPropagation();
                            openNote(destination.id);
                          }}
                          className="text-green-500 h-7 hover:text-green-700 justify-end"
                        >
                          <img src="/notes_icon.png" alt="Notizen" className="h-7 hover:scale-115 cursor-pointer" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}

      </div>

      {/* Add and Reorder */}
      <AnimatePresence mode="wait">
        {isReorderMode ? (
          <motion.div
            key="save-button"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3 }}
            className="flex justify-center mt-6"
          >
            <button
              onClick={saveNewOrder}
              className={`px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 cursor-pointer`}
            >
              💾 Save
            </button>
          </motion.div>
        ) : (
          <motion.div
            key="add-button"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 0.3, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3 }}
            className="flex justify-center mt-4"
          >
            <button
              onClick={handleAddClick}
              className="transition-opacity opacity-70 hover:opacity-100 hover:scale-115 duration-300 cursor-pointer"
            >
              <img src="/plus_icon.png" alt="Add Destination" className="w-12 h-12" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Delete Destination */}
      {confirmDeleteId && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-80">
            <h2 className="text-lg font-semibold mb-4">Destination löschen?</h2>
            <p className="mb-4 text-sm text-gray-600">
              Bist du sicher, dass du diese Destination löschen möchtest? Dies kann nicht rückgängig gemacht werden.
            </p>
            <div className="flex justify-end space-x-4">
              <button
                className="px-4 py-2 text-gray-600 hover:text-black"
                onClick={() => setConfirmDeleteId(null)}
              >
                Abbrechen
              </button>
              <button
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                onClick={async () => {
                  setDeleting(true);
                  try {
                    const response = await fetch(`${BASE_URL}/destination/delete/${confirmDeleteId}`, {
                      method: 'DELETE',
                      credentials: 'include',
                    });
                    if (!response.ok) throw new Error('Fehler beim Löschen');
                    setDestinations(destinations.filter((dest) => dest.id !== confirmDeleteId));
                    setConfirmDeleteId(null);
                  } catch (err) {
                    alert('Löschen fehlgeschlagen.');
                  } finally {
                    setDeleting(false);
                  }
                }}
                disabled={deleting}
              >
                {deleting ? 'Lösche...' : 'Ja, löschen'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Show notes */}
      {noteForId && (
        <div data-ignore-click className="fixed inset-0 flex items-center justify-center bg-black/20 z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-[90%] max-w-md relative">
            <h2 className="text-lg font-semibold mb-4">Notizen zur Destination</h2>

            {!editingNote ? (
              <>
                <div className="whitespace-pre-wrap text-sm text-gray-800 overflow-y-auto max-h-64">
                  {
                    // Auto-Linking von URLs
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
                  }
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
                      const d = destinations.find((d) => d.id === noteForId);
                      setNoteText(d?.free_text || '');
                    }}
                  >
                    Abbrechen
                  </button>
                  <button
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                    onClick={saveNote}
                    disabled={savingNote}
                  >
                    {savingNote ? 'Speichere...' : 'Speichern'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DestinationsPage;