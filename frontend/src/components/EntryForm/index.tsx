import { useState, useEffect } from 'react';
import { toast } from 'sonner';

import ImageSearchModal from './ImageSearchModal';
import TagsInput from './TagsInput';
import Form from '../Form/Form';
import Button from '../Buttons/Button';
import CancelButton from '../Buttons/CancelButton';
import InputField from '@/components/Form/InputField';
import FormSubmitButton from '@/components/Buttons/FormSubmitButton';
import { useImageSearch } from '@/hooks/useImageSearch';
import { useEntryFormState } from '@/hooks/useEntryFormState';
import { validateTitleField } from '@/utils/formValidations';

interface EntryFormProps {
  type: 'destination' | 'activity';
  onSubmit: (data: any) => Promise<void>;
  submitLabel: string;
  initialData?: {
    title?: string;
    country?: string; // destination only
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
    removeTag,
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

  const [isSaving, setIsSaving] = useState(false);

  // Errors
  const titleErrors = validateTitleField(title);
  const isDisabled = titleErrors.length > 0 || isSaving;

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

  // Submit
  const handleFormSubmit = async (e: React.FormEvent) => {

    e.preventDefault();

    // Handle errors
    if (titleErrors.length > 0) {
      titleErrors.forEach((err) => toast.error(err));
      return;
    }

    setIsSaving(true);

    const formData = {
      title,
      country,
      img_link: selectedImageUrl,
      tags: tagsArray.join(', '),
    };

    await onSubmit(formData);
    setIsSaving(false);
  };

  return (
    <Form onSubmit={handleFormSubmit}>

      {/* Title */}
      <InputField
        label="Title"
        type="text"
        value={title}
        placeholder="Paris, New York, Tokyo, ..."
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      {/* Country */}
      {type === 'destination' && (
        <InputField
          label="Country"
          type="text"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />
      )}

      {/* Search Image */}
      <div className="">
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

          <Button
            text="SearchImage"
            type="button"
            onClick={searchImages}
            isDisabled={!imageSearchTerm.trim()}
          />

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
      <FormSubmitButton
        text={isSaving ? 'Saving...' : submitLabel}
        isDisabled={isDisabled}
      />

      {/* Cancel button */}
      <CancelButton href="/destination/get_all" />

    </Form>
  );
};

export default EntryForm;