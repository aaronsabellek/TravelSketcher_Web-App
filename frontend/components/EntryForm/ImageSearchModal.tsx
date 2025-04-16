import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion'
import { useImageSearch } from '../../hooks/useImageSearch';

// Animation funktioniert nicht beim Zuklappen

interface UnsplashImage {
  id: string;
  url: string;
  alt_description: string;
}

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

const ImageSearchModal: React.FC<ImageSearchModalProps> = ({
  tempSelectedImageUrl,
  imageSearchTerm,
  setImageSearchTerm,
  closeModal,
  isModalOpen,
  searchImages,
  handleImageSelect,
  handleConfirmSelection,
  imageResults,
  isSearching,
  loadMoreImages,
  loadingMore,
  scrollContainerRef,
  modalRef,
}) => {

  // Holen der handleScroll-Funktion vom useImageSearch Hook
  const { handleScroll, isAtBottom } = useImageSearch();

  // Handle modal close on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
        closeModal();
      }
    };

    if (isModalOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [isModalOpen, closeModal, modalRef]);


  return isModalOpen ? (
    <AnimatePresence>
          <div
            className="fixed inset-0 flex justify-center items-center z-50"
          >
            <motion.div
              ref={modalRef}
              className={`relative w-full md:w-2/3 lg:w-1/2 xl:w-1/3 bg-white rounded-lg p-6 z-50 border border-gray-300 rounded-md shadow-sm`}
              initial={{ opacity: 0 }} // Modal beginnt unsichtbar
              animate={{ opacity: 1 }} // Modal wird sichtbar
              exit={{ opacity: 0 }} // Modal wird unsichtbar, wenn es schließt
              transition={{ duration: 0.5, ease: 'easeInOut' }}
            >
            <h2 className="text-lg font-semibold mb-4">Wähle ein Bild</h2>

            {isSearching && <p>Suche läuft...</p>}

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
                //onClick={() => setIsModalOpen(false)}
                onClick={closeModal}
                className="px-4 py-2 bg-gray-300 rounded-lg mt-4 hover:bg-gray-400"
              >
                Abbrechen
              </button>
              <button
                onClick={handleConfirmSelection}
                disabled={!tempSelectedImageUrl}
                className={`py-2 px-4 mt-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 ${
                  tempSelectedImageUrl ? '' : 'opacity-50 cursor-not-allowed'
                }`}
              >
                Select
              </button>
                {imageResults.length > 0 && !isSearching && (
                  <button
                    onClick={loadMoreImages}
                    disabled={!isAtBottom || loadingMore}
                    className={`py-2 px-4 mt-4 rounded-lg bg-blue-500 text-white hover:bg-blue-600 ${
                      (isAtBottom && !loadingMore) ? '' : 'opacity-50 cursor-not-allowed'
                    }`}
                  >
                    Mehr Bilder laden
                  </button>
                )}
              </div>
            </motion.div>
          </div>
          </AnimatePresence>
  ) : null;
};

export default ImageSearchModal;