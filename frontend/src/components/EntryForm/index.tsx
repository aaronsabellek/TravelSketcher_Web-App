import { useEffect } from 'react';

import ImageSearchModal from './ImageSearchModal';
import TagsInput from './TagsInput';
import { useImageSearch } from '@/hooks/useImageSearch';
import { useEntryFormState } from '@/hooks/useEntryFormState';

interface EntryFormProps {
  type: 'destination' | 'activity';
  onSubmit: (data: any) => Promise<void>;
  submitLabel: string;
  initialData?: {
    title?: string;
    country?: string; // destination only
    status?: 'planned' | 'done';
    tags?: string[];
    img_link?: string;
  };
}

// Adds or edits an entry
const EntryForm: React.FC<EntryFormProps> = ({ type, onSubmit, initialData, submitLabel }) => {

  const {
    title,
    setTitle,
    country,
    setCountry,
    tagInput,
    setTagInput,
    tagsArray,
    setTagsArray,
    selectedImageUrl,
    setSelectedImageUrl,
    isSaving,
    removeTag,
    handleFormSubmit,
  } = useEntryFormState({ type, initialData, onSubmit });

  const {
    updateTitle,
    selectedImageUrl: imageSearchSelectedImageUrl,
    handleImageSelect,
    imageSearchTerm,
    tempSelectedImageUrl,
    setTempSelectedImageUrl,
    setSelectedImageUrl: setImageSearchSelectedImageUrl,
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

  // Sync entry title with image search
  useEffect(() => {
    if (title) updateTitle(title);
  }, [title, updateTitle]);

  // Select image
  useEffect(() => {
    if (imageSearchSelectedImageUrl) {
      setSelectedImageUrl(imageSearchSelectedImageUrl);
    }
  }, [imageSearchSelectedImageUrl]);

  return (
    <form onSubmit={handleFormSubmit}>

      {/* Title */}
      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title (<span className="text-red-500">*</span>required)
        </label>
        <input
            type="text"
            id="title"
            value={title}
            placeholder="Paris, New York, Tokyo, ..."
            onChange={(e) => setTitle(e.target.value)}
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
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm bg-white"
          />
        </div>
      )}

      {/* Search Image */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Image
        </label>
        {selectedImageUrl && (
          <div className="flex justify-center">
            <img
                src={selectedImageUrl}
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
        tagInput={tagInput}
        setTagInput={setTagInput}
        tagsArray={tagsArray}
        setTagsArray={setTagsArray}
        onRemoveTag={removeTag}
      />

      {/* ImageSearch Modal */}
      <ImageSearchModal
        selectedImageUrl={imageSearchSelectedImageUrl}
        tempSelectedImageUrl={tempSelectedImageUrl}
        setSelectedImageUrl={setImageSearchSelectedImageUrl}
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
          disabled={!title.trim() || isSaving}
          className={`py-2 px-4 font-light rounded-lg cursor-pointer transition ${
            !title.trim() || isSaving
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-500 text-white hover:bg-blue-600'
          }`}
        >
          {isSaving ? 'Saving...' : submitLabel}
        </button>
      </div>

    </form>
  );
};

export default EntryForm;