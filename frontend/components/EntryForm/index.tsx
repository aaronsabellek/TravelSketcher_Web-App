import { useState, useEffect } from 'react';
import { useEntryForm } from '../../hooks/useEntryForm';
import { useImageSearch } from '../../hooks/useImageSearch';
import ImageSearchModal from './ImageSearchModal';
import TagsInput from './TagsInput';

// Automatisches Weiterladen von Bildern

// Props-Typ definieren
interface EntryFormProps {
  onSubmit: (data: any) => void;
  initialData?: {
    title?: string;
    country?: string;
    status?: 'planned' | 'done';
    tags?: string[];
    imageUrl?: string;
  };
  submitLabel: string;
}

const EntryForm: React.FC<EntryFormProps> = ({ onSubmit, initialData, submitLabel }) => {
  const form = useEntryForm({ onSubmit, initialData });
  const {
    updateTitle, // Titel aktualisieren
    selectedImageUrl,
    handleImageSelect,
    imageSearchTerm,
    tempSelectedImageUrl,
    setTempSelectedImageUrl,
    setSelectedImageUrl,
    setImageSearchTerm,
    searchImages,
    handleConfirmSelection,
    isModalOpen,
    openModal,
    closeModal,
    imageResults,
    isSearching,
    loadMoreImages,
    isAtBottom,
    loadingMore,
    scrollContainerRef,
    modalRef,
    setHasManuallyEditedSearch,
  } = useImageSearch();

  // Den title an den Hook übergeben, wenn er sich ändert
  useEffect(() => {
    if (form.title) {
      updateTitle(form.title); // Titel im Hook aktualisieren
    }
  }, [form.title, updateTitle]); // Hook wird jedes Mal aufgerufen, wenn sich der title ändert

  // Wenn ein Bild aus der Bildsuche ausgewählt wurde, ins Formular übernehmen
  useEffect(() => {
    if (selectedImageUrl) {
      form.setSelectedImageUrl(selectedImageUrl); // Bild ins Formular übernehmen
    }
  }, [selectedImageUrl, form]);

  return (
    <form onSubmit={form.handleSubmit}>
      {/* Title Field */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Title</label>
        <input
          type="text"
          value={form.title}
          onChange={(e) => form.setTitle(e.target.value)}
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      {/* Country Field */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Country</label>
        <input
          type="text"
          value={form.country}
          onChange={(e) => form.setCountry(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        />
      </div>

      {/* Selected image */}
      {form.selectedImageUrl && (
        <div className="mb-4">
          <img src={form.selectedImageUrl} alt="Ausgewähltes Bild" className="w-full max-h-60 object-cover rounded" />
        </div>
      )}

      {/* Image search field & button */}
      <div className="flex gap-2">
          <input
              type="text"
              value={imageSearchTerm}
              onChange={(e) => {
                setImageSearchTerm(e.target.value);
                setHasManuallyEditedSearch(true);
                }}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          />
          <button
              type="button"
              onClick={searchImages}
              disabled={!imageSearchTerm.trim()}
              className={`py-2 px-4 bg-blue-500 text-white rounded-md transition cursor-pointer hover:bg-blue-600 ${
                imageSearchTerm.trim()
                    ? 'hover:bg-blue-600'
                    : 'opacity-50 cursor-not-allowed'
                }`}
          >
              Search Image
          </button>
      </div>

      {/* Tags Input */}
      <TagsInput
        tagInput={form.tagInput}
        setTagInput={form.setTagInput}
        tagsArray={form.tagsArray}
        setTagsArray={form.setTagsArray}
        onRemoveTag={form.removeTag}
      />

      {/* Status Dropdown */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Status</label>
        <select
          value={form.status}
          onChange={(e) => form.setStatus(e.target.value as 'planned' | 'done')}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
        >
          <option value="planned">Planned</option>
          <option value="done">Done</option>
        </select>
      </div>

      {/* ImageSearch Modal */}
      <ImageSearchModal
        selectedImageUrl={selectedImageUrl}
        tempSelectedImageUrl={tempSelectedImageUrl}
        setSelectedImageUrl={setSelectedImageUrl}
        setTempSelectedImageUrl={setTempSelectedImageUrl}
        imageSearchTerm={imageSearchTerm}
        setImageSearchTerm={setImageSearchTerm}
        openModal={openModal}
        closeModal={closeModal}
        isModalOpen={isModalOpen}
        searchImages={searchImages}
        handleImageSelect={handleImageSelect}
        handleConfirmSelection={handleConfirmSelection}
        imageResults={imageResults}
        isSearching={isSearching}
        loadMoreImages={loadMoreImages}
        isAtBottom={isAtBottom}
        loadingMore={loadingMore}
        scrollContainerRef={scrollContainerRef as React.RefObject<HTMLDivElement>}
        modalRef={modalRef as React.RefObject<HTMLDivElement>}
      />

      {/* Submit Button */}
      <div className="flex justify-center mt-6">
        <button
          type="submit"
          disabled={!form.title.trim() || form.isSaving}
          className={`py-2 px-4 rounded-lg text-white transition ${
            form.isSaving || !form.title.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {form.isSaving ? 'Speichern…' : submitLabel}
        </button>
      </div>
    </form>
  );
};

export default EntryForm;