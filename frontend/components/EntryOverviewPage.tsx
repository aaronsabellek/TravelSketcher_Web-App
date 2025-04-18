import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { useRedirectIfNotAuthenticated } from '../utils/authRedirects';
import Link from 'next/link';
import { BASE_URL, default_img } from '../utils/config';
import { Destination, Activity } from '../types/models';
import { useDestinations } from '../hooks/useDestinations';
import { useUserCity } from '../hooks/useUserCity';
import { useDestinationActions } from '../hooks/useDestinationActions';
import DestinationCard from './DestinationCard';
import NoteModal from './NoteModal';
import DeleteConfirmModal from './DeleteConfirmModal';
import AddOrReorderButton from './AddOrReorderButton';
import { useReorder } from '../hooks/useReorder';
import { useClickOutsideMenu } from '../hooks/useClickOutsideMenu'

interface EntryOverviewPageProps<T> {
  title: string;
  fetchHook: () => {
    items: T[];
    setItems: React.Dispatch<React.SetStateAction<T[]>>;
    loading: boolean;
    error: string | null;
  };
  addRoute: string;
  showUserCity?: boolean;
  isActivityPage?: boolean;
}

const EntryOverviewPage = <T extends Destination | Activity>({
  title,
  fetchHook,
  addRoute,
  showUserCity = false,
  isActivityPage = false,
}: EntryOverviewPageProps<T>) => {

  const router = useRouter();
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const { items, setItems, loading, error } = fetchHook();
  const { city: userCity } = useUserCity();
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
  } = useDestinationActions<T>(items, setItems);

  const {
    isReorderMode,
    toggleReorderMode,
    moveDestinationUp,
    moveDestinationDown,
    saveNewOrder,
    hasOrderChanged,
  } = useReorder<T>(items, setItems);

  useRedirectIfNotAuthenticated();
  useClickOutsideMenu(menuRef, !!menuOpenFor, () => setMenuOpenFor(null));

  const handleAddClick = () => {
    router.push(addRoute);
  };

  return (
    <div className="container max-w-6xl mx-auto px-4">
      <h1 className="text-3xl font-bold mb-2">{title}</h1>

      <div className="flex justify-between mb-3">
        <button
          onClick={toggleReorderMode}
          className="px-3 py-1 text-xl cursor-pointer transition-all duration-300 ease-in-out transform active:scale-95 hover:scale-115"
        >
          <img src="/change_icon.png" className="h-7" />
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {items.map((item, index) => (
          <DestinationCard
            key={item.id}
            data={item}
            isExpanded={expandedCard === item.id}
            onExpand={() => setExpandedCard(item.id)}
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
            items={items}
            setExpandedCard={setExpandedCard}
            userCity={showUserCity ? userCity : null}
          />
        ))}
      </div>

      <AddOrReorderButton
        isReorderMode={isReorderMode}
        hasOrderChanged={hasOrderChanged}
        saveNewOrder={saveNewOrder}
        handleAddClick={handleAddClick}
      />

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
            setItems(items.filter((item) => item.id !== confirmDeleteId));
            setConfirmDeleteId(null);
          } catch (err) {
            alert('Löschen fehlgeschlagen.');
          } finally {
            setDeleting(false);
          }
        }}
        deleting={deleting}
      />

      <NoteModal
        noteText={noteText}
        setNoteText={setNoteText}
        editingNote={editingNote}
        setEditingNote={setEditingNote}
        noteForId={noteForId}
        setNoteForId={setNoteForId}
        saveNote={saveNote}
        items={items}
        setItems={setItems}
      />
    </div>
  );
};

export default EntryOverviewPage;