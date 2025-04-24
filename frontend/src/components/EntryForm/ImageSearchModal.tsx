import React from 'react';
import { motion, AnimatePresence } from 'framer-motion'

import { useClickOutside } from '@/hooks/useClickOutside';
import { UnsplashImage } from '@/types/models';

interface ImageSearchModalProps {
  selectedImageUrl: string;
  tempSelectedImageUrl: string | null;
  setSelectedImageUrl: (url: string) => void;
  setTempSelectedImageUrl: (url: string | null) => void;
  imageSearchTerm: string;
  setImageSearchTerm: (term: string) => void;
  openModal: () => void;
  closeModal: () => void;
  isModalOpen: boolean;
  handleScroll: (e: React.UIEvent<HTMLDivElement, UIEvent>) => void;
  searchImages: () => void;
  handleImageSelect: (url: string) => void;
  handleConfirmSelection: () => void;
  imageResults: UnsplashImage[];
  isSearching: boolean;
  loadMoreImages: () => void;
  isAtBottom: boolean;
  loadingMore: boolean;
  scrollContainerRef: React.RefObject<HTMLDivElement>;
  modalRef: React.RefObject<HTMLDivElement>;
}

// Opens a window to show and select an image from Unsplash for an entry
const ImageSearchModal: React.FC<ImageSearchModalProps> = ({
  tempSelectedImageUrl,
  closeModal,
  isModalOpen,
  handleScroll,
  handleImageSelect,
  handleConfirmSelection,
  imageResults,
  isSearching,
  scrollContainerRef,
  modalRef,
}) => {

  // Close image modal with click outside
  useClickOutside([modalRef], closeModal, isModalOpen);

  return (
    <AnimatePresence>
      {isModalOpen && (
        <div
          className="fixed inset-0 flex justify-center items-center z-50"
        >
          <motion.div
            ref={modalRef}
            className={`relative w-full md:w-2/3 lg:w-1/2 xl:w-1/3 bg-white rounded-lg p-6 z-50 border border-gray-300 rounded-md shadow-sm`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5, ease: 'easeInOut' }}
          >
          <h2 className="text-lg font-semibold mb-4">Choose an image</h2>

          {isSearching && <p>Searching...</p>}

          <div
              className="grid grid-cols-3 gap-4 max-h-96 overflow-y-auto"
              onScroll={handleScroll}
              ref={scrollContainerRef}
          >

            {/* Image */}
            {imageResults.map((img) => (
              <div
                key={img.id}
                className={`relative cursor-pointer rounded-md overflow-hidden border-2 ${
                  tempSelectedImageUrl === img.url
                  ? 'border-blue-500'
                  : 'border-transparent'
                }`}
                onClick={() => handleImageSelect(img.url)}
              >
                <div className="aspect-[16/12] w-full">
                  <img
                    src={img.url}
                    alt={img.alt_description || 'Bild'}
                    className="object-cover w-full h-full"
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Buttons */}
          <div className="mt-6 flex justify-end gap-2">
            <button
              type="button"
              onClick={closeModal}
              className="px-4 py-2 bg-gray-300 rounded-lg mt-4 hover:bg-gray-400"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleConfirmSelection}
              disabled={!tempSelectedImageUrl}
              className={`py-2 px-4 mt-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 ${
                tempSelectedImageUrl ? '' : 'opacity-50 cursor-not-allowed'
              }`}
            >
              Select
            </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default ImageSearchModal;