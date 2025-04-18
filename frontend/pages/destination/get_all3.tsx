import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';
import Link from 'next/link';
import { BASE_URL, default_img } from '../../utils/config';
import { Destination } from '../../types/models';
import { useDestinations } from '../../hooks/useDestinations';
import { useUserCity } from '../../hooks/useUserCity';
import { useDestinationActions } from '../../hooks/useDestinationActions';
import DestinationCard from '../../components/DestinationCard';
import NoteModal from '../../components/NoteModal';
import DeleteConfirmModal from '../../components/DeleteConfirmModal';
import AddOrReorderButton from '../../components/AddOrReorderButton';
import { useReorder } from '../../hooks/useReorder';
import { useClickOutsideMenu } from '../../hooks/useClickOutsideMenu'


const DestinationsPage = () => {

  // Router
  const router = useRouter();

  // Expand card
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  // Abrufen der Destinations
  const { destinations, setDestinations, loading, error } = useDestinations();

  // Get city from user
  const { city: userCity, loading: cityLoading } = useUserCity();

  // Destination Actions
  const {
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
  } = useDestinationActions(destinations, setDestinations);

  // Reorder
  const {
    isReorderMode,
    toggleReorderMode,
    moveDestinationUp,
    moveDestinationDown,
    saveNewOrder,
    hasOrderChanged,
  } = useReorder(destinations, setDestinations);

  // Redirect if user is not logged in
  useRedirectIfNotAuthenticated();

  // Add destination
  const handleAddClick = () => {
    router.push('/destination/add');
  };

  // Close edit/delete window with clicks outside
  useClickOutsideMenu(menuRef, !!menuOpenFor, () => setMenuOpenFor(null));

  return (
    <div className="container max-w-6xl mx-auto px-4">

      {/* Header */}
      <h1 className="text-3xl font-bold mb-2">My Destinations</h1>

      {/* Button zum Aktivieren des Reorder-Modus */}
      <div className="flex justify-between mb-3">
        <button
          onClick={toggleReorderMode}
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
          {destinations.map((destination, index) => (
            <DestinationCard
              key={destination.id}
              data={destination}
              isExpanded={expandedCard === destination.id}
              onExpand={() => setExpandedCard(destination.id)}
              onCollapse={() => setExpandedCard(null)}
              onEdit={handleEdit}
              onDelete={handleDeleteConfirm}
              onNote={openNote}
              menuOpenFor={menuOpenFor}
              setMenuOpenFor={setMenuOpenFor}
              menuRef={menuRef}
              default_img={default_img}
              isReorderMode={isReorderMode}
              index={index}
              moveDestinationUp={moveDestinationUp}
              moveDestinationDown={moveDestinationDown}
              destinations={destinations}
              setExpandedCard={setExpandedCard}
              userCity={userCity}
            />
            //const isExpanded = expandedCard === destination.id;
          ))}
      </div>

      {/* Add and Reorder */}
      <AddOrReorderButton
        isReorderMode={isReorderMode}
        hasOrderChanged={hasOrderChanged}
        saveNewOrder={saveNewOrder}
        handleAddClick={handleAddClick}
      />

      {/* Delete Destination */}
      <DeleteConfirmModal
        isOpen={!!confirmDeleteId}
        onClose={() => setConfirmDeleteId(null)}
        onDelete={async () => {
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
        deleting={deleting}
      />

      {/* Show notes */}
      <NoteModal
        noteText={noteText}
        setNoteText={setNoteText}
        editingNote={editingNote}
        setEditingNote={setEditingNote}
        noteForId={noteForId}
        setNoteForId={setNoteForId}
        saveNote={saveNote}
        destinations={destinations}
        setDestinations={setDestinations}
      />
    </div>
  );
};

export default DestinationsPage;