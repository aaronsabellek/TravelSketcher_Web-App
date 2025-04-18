import { useState, useEffect } from 'react';
import { useEntryForm } from '../../hooks/useEntryForm';
import { useImageSearch } from '../../hooks/useImageSearch';
import ImageSearchModal from './ImageSearchModal';
import TagsInput from './TagsInput';
import { useFormSync } from '../../hooks/useFormSync';

// Props-Typ definieren
interface EntryFormProps {
  type: 'destination' | 'activity';
  onSubmit: (data: any) => void;
  initialData?: {
    title?: string;
    country?: string; // Nur für Destination
    status?: 'planned' | 'done';
    tags?: string[];
    img_link?: string;
  };
  submitLabel: string;
}

const EntryForm: React.FC<EntryFormProps> = ({ type, onSubmit, initialData, submitLabel }) => {
  const form = useEntryForm({ onSubmit, initialData });

  // When edit: Load data
  useEffect(() => {
    if (!initialData) return;
      if (initialData.title) form.setTitle(initialData.title);
      if (initialData.country) form.setCountry(initialData.country);
      if (initialData.status) form.setStatus(initialData.status);
      if (initialData.tags) form.setTagsArray(initialData.tags);
      if (initialData.img_link) form.setSelectedImageUrl(initialData.img_link);
  }, [initialData]);

  const {
    updateTitle,
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
    handleScroll,
    imageResults,
    isSearching,
    loadMoreImages,
    isAtBottom,
    loadingMore,
    scrollContainerRef,
    modalRef,
    setHasManuallyEditedSearch,
  } = useImageSearch();

  // Sync title with image search
  useFormSync({ form, selectedImageUrl, updateTitle });

  return (
    <form onSubmit={form.handleFormSubmit}>

      {/* Title */}
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title (<span className="text-red-500">*</span>required)
        </label>
        <input
            type="text"
            id="title"
            value={form.title}
            placeholder="Paris, New York, Tokyo, ..."
            onChange={(e) => form.setTitle(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
        />
      </div>

      {/* Country */}
      {type === 'destination' && (
        <div className="mb-4">
          <label htmlFor="country" className="block text-sm font-medium text-gray-700">
            Country
          </label>
          <input
              type="text"
              id="country"
              value={form.country}
              onChange={(e) => form.setCountry(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-white"
          />
        </div>
      )}

      {/* Search Image */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Image
        </label>
        {form.selectedImageUrl && (
          <div className="flex justify-center">
            <img
                src={form.selectedImageUrl}
                alt="Ausgewähltes Bild"
                className="w-[280px] aspect-[16/12] object-cover rounded-lg mb-2 border border-gray-300 overflow-hidden"
            />
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
        <label
          htmlFor="status"
          className="block text-sm font-medium text-gray-700"
        >
          Status
        </label>
        <select
          id="status"
          value={form.status}
          onChange={(e) => form.setStatus(e.target.value as 'planned' | 'done')}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
        >
          <option value="planned">planned</option>
          <option value="done">done</option>
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
        handleScroll={handleScroll}
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
      <div className="flex justify-center items-center">
        <button
          type="submit"

          disabled={!form.title.trim() || form.isSaving}
          className={`py-2 px-4 font-light rounded-lg cursor-pointer transition ${
            !form.title.trim() || form.isSaving
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-500 text-white hover:bg-blue-600'
          }`}
        >
          {form.isSaving ? 'Saving...' : submitLabel}
        </button>
      </div>

    </form>
  );
};

export default EntryForm;