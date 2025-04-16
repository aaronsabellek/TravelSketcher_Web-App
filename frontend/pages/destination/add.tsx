import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/router';
import Container from '../../components/Container';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'framer-motion'
import BASE_URL from '../../utils/config';

// Image objects from Unsplash
interface UnsplashImage {
    id: string;
    url: string;
    alt_description: string;
  }

const AddDestination = () => {
  const router = useRouter();

  const [title, setTitle] = useState('');
  const [country, setCountry] = useState('');
  const [status, setStatus] = useState<'planned' | 'done'>('planned');

  // Tags
  const [tagInput, setTagInput] = useState('');
  const [tagsArray, setTagsArray] = useState<string[]>([]);

  const [isSaving, setIsSaving] = useState(false);

  // Image
  const [imageSearchTerm, setImageSearchTerm] = useState('');
  const [hasManuallyEditedSearch, setHasManuallyEditedSearch] = useState(false);
  const [imageResults, setImageResults] = useState<UnsplashImage[]>([]);
  const [selectedImageUrl, setSelectedImageUrl] = useState('');
  const [tempSelectedImageUrl, setTempSelectedImageUrl] = useState<string | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [loadingMore, setLoadingMore] = useState(false);
  const [isAtBottom, setIsAtBottom] = useState(false);

  // Refs
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const modalRef = useRef<HTMLDivElement | null>(null);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  // Synchronise fields for 'title' and 'image'
  useEffect(() => {
    if (!hasManuallyEditedSearch) {
      setImageSearchTerm(title);
    }
  }, [title]);

  // Handler for Submission of form
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSaving(true);
    try {
      const response = await fetch(`${BASE_URL}/destination/add`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          country,
          img_link: selectedImageUrl || '',
          status,
          tags: tagsArray.join(','),
        }),
      });

      if (!response.ok) throw new Error('Fehler beim Speichern');
      toast.success('Destination erfolgreich hinzugefügt!');
      router.push('/destination/get_all');
    } catch (err) {
      console.error(err);
      toast.error('Fehler beim Speichern der Destination.');
    } finally {
      setIsSaving(false);
    }
  };

  // Handle tag layout
  const handleTagKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === ',' || e.key === 'Enter') {
      e.preventDefault();
      const newTag = tagInput.trim().replace(/,$/, '');
      if (newTag && !tagsArray.includes(newTag)) {
        setTagsArray([...tagsArray, newTag]);
      }
      setTagInput('');
    }
  };

  // Remove tag
  const removeTag = (tagToRemove: string) => {
    setTagsArray(tagsArray.filter(tag => tag !== tagToRemove));
  };

  // Funktion zum Schließen des Modals, wenn außerhalb geklickt wird
  const handleClickOutside = (e: MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
    closeModal(); // Modal schließen, wenn außerhalb geklickt wird
    }
  };

  useEffect(() => {
    if (isModalOpen) {
      // Eventlistener hinzufügen, wenn das Modal geöffnet ist
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        // Eventlistener entfernen, wenn das Modal geschlossen wird
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [isModalOpen]);

  // Select image
  const handleImageSelect = (imageUrl: string) => {
    setTempSelectedImageUrl(imageUrl);
  };

  // Confirm image selection
  const handleConfirmSelection = () => {
    if (tempSelectedImageUrl) {
      setSelectedImageUrl(tempSelectedImageUrl); // Setzt das endgültig ausgewählte Bild, wenn es nicht null ist
      setTempSelectedImageUrl(null);
      setIsModalOpen(false); // Schließt das Modal
    } else {
      console.error("Kein Bild ausgewählt");
    }
  };

  // Search images
  const searchImages = async () => {
    if (!imageSearchTerm) return;
    setIsSearching(true);
    setCurrentPage(1); // Back to page 1
    try {
        const response = await fetch(
            `${BASE_URL}/search-images?query=${encodeURIComponent(imageSearchTerm)}&page=1`
          );
      const data = await response.json();
      setImageResults(data.results);
      setIsModalOpen(true);
    } catch (err) {
      console.error('Fehler bei der Bildsuche:', err);
    } finally {
      setIsSearching(false);
    }
  };

  // Handle scroll position
  const handleScroll = (e: React.UIEvent<HTMLDivElement, UIEvent>) => {
    const bottom = e.currentTarget.scrollHeight === e.currentTarget.scrollTop + e.currentTarget.clientHeight;
    setIsAtBottom(bottom); // Wenn das Ende erreicht ist, setzen wir isAtBottom auf true
  };

  // Load more images
  const loadMoreImages = async () => {
    if (!loadingMore) {
        setLoadingMore(true); // Disable button
        setIsAtBottom(false);

        const nextPage = currentPage + 1;

        try {
            const response = await fetch(
              `${BASE_URL}/search-images?query=${encodeURIComponent(imageSearchTerm)}&page=${nextPage}`
            );
            const data = await response.json();
            setImageResults((prevResults) => [...prevResults, ...data.results]);
            setCurrentPage(nextPage); // Seite erhöhen
          } catch (err) {
            console.error('Fehler beim Laden weiterer Bilder:', err);
          } finally {
            setLoadingMore(false);
          }
    }
  };


  return (
    <Container title="Add destination">

      {/* Add destination form */}
      <form onSubmit={handleSubmit}>

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
        <div className="mb-4">
        <label htmlFor="country" className="block text-sm font-medium text-gray-700">Country</label>
        <input
            type="text"
            id="country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
        />
        </div>

        {/* Image */}
        <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Image</label>

            {/* Image preview */}
            {selectedImageUrl && (
                <img
                    src={selectedImageUrl}
                    alt="Ausgewähltes Bild"
                    className="w-full h-auto aspect-[16/12] object-cover rounded-md mb-2 border"
                />
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

        {/* Tags */}
        <div className="mb-4">
            <label htmlFor="tags" className="block text-sm font-medium text-gray-700">Tags</label>
            <input
                type="text"
                id="tags"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleTagKeyDown}
                placeholder="Seperate with commas"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
            />
            <div className="mt-2 flex flex-wrap">
                {tagsArray.map((tag) => (
                    <span
                        key={tag}
                        className="text-xs bg-gray-200 rounded-full px-2 py-1 mr-2 mb-1 inline-flex items-center"
                    >
                        {tag}
                        <button
                            type="button"
                            onClick={() => removeTag(tag)}
                            className="ml-1 text-gray-500 hover:text-red-500"
                        >
                            &times;
                        </button>
                    </span>
                ))}
            </div>
        </div>

        {/* Status dropdown */}
        <div className="mb-4">
          <label htmlFor="status" className="block text-sm font-medium text-gray-700">Status</label>
          <select
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value as 'planned' | 'done')}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
          >
            <option value="planned">planned</option>
            <option value="done">done</option>
          </select>
        </div>

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
            {isSaving ? 'Speichern...' : 'Destination speichern'}
          </button>
        </div>
      </form>

      {/* Search Image window */}
        {isModalOpen && (
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
        )}
    </Container>
  );
};

export default AddDestination;