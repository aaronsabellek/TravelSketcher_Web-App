import React, { useState } from 'react';
import { useRouter } from 'next/router';

import EntryCard from './EntryCard';
import NoteModal from './NoteModal';
import DeleteConfirmModal from './DeleteConfirmModal';
import WebLinkModal from './WebLinkModal';
import AddOrReorderButton from './AddOrReorderButton';
import { BASE_URL, default_img } from '../../utils/config';
import { Destination, Activity } from '../../types/models';
import { useReorder } from '../../hooks/useReorder';
import { useUserCity } from '../../hooks/useUserCity';
import { useEntryActions } from '../../hooks/useEntryActions';
import { useClickOutside } from '../../hooks/useClickOutside';

interface EntryOverviewPageProps<T> {
  title: string;
  addRoute: string;
  routeBase: string;
  type: 'destination' | 'activity';
  showUserCity?: boolean;
  isActivityPage?: boolean;
  fetchHook: () => {
    items: T[];
    setItems: React.Dispatch<React.SetStateAction<T[]>>;
    loading: boolean;
    error: string | null;
    loadMore?: () => void;
    hasMore?: boolean;
    loadingMore?: boolean;
    handleScroll?: (e: React.UIEvent<HTMLDivElement>) => void;
  };
}

const EntryOverviewPage = <T extends Destination | Activity>({
  title,
  fetchHook,
  addRoute,
  routeBase,
  type,
  showUserCity = false,
}: EntryOverviewPageProps<T>) => {

  const router = useRouter();
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const [webLink, setWebLink] = useState('');
  const [editingLink, setEditingLink] = useState(false);
  const [linkForId, setLinkForId] = useState<string | null>(null);

  const {
    items,
    setItems,
    loading,
    error,
    loadingMore,
  } = fetchHook();

  // Get city from user for rom2rio-link
  const { city } = useUserCity();

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
  } = useEntryActions<T>(items, setItems, routeBase);

  const {
    isReorderMode,
    toggleReorderMode,
    moveDestinationUp,
    moveDestinationDown,
    saveNewOrder,
    hasOrderChanged,
  } = useReorder<T>(type, items, setItems);

  useClickOutside(menuRef, () => setMenuOpenFor(null), !!menuOpenFor)

  const handleAddClick = () => {
    router.push(addRoute);
  };

  return (
    <div className="">
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

      <div className="grid grid-cols-1 xs:grid-cols-2 md:grid-cols-3 gap-4">
        {items.length === 0 ? (
          <div className="col-span-1 xs:col-span-2 md:col-span-3 text-center p-4 text-gray-500">
            No entries yet. Click the add button and start your journey!
          </div>
        ) : (
          items.map((item, index) => (
            <EntryCard
              key={item.id}
              data={item}
              type={type}
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
              onLinkClick={(id, web_link) => {
                setLinkForId(id);
                setWebLink(web_link || '');
                setEditingLink(false);
              }}
              userCity={showUserCity ? city : null}
            />
            ))
        )}
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
            const response = await fetch(`${BASE_URL}/${routeBase}/delete/${confirmDeleteId}`, {
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
        itemType={type}
      />

      <NoteModal
        type={type}
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

      <WebLinkModal
        items={items}
        setItems={setItems}
        webLink={webLink}
        setWebLink={setWebLink}
        editingLink={editingLink}
        setEditingLink={setEditingLink}
        linkForId={linkForId}
        setLinkForId={setLinkForId}
      />

      {loadingMore && (
        <div className="col-span-2 md:col-span-3 text-center py-4 text-gray-400">
          Loading more entries...
        </div>
      )}
    </div>
  );
};

export default EntryOverviewPage;