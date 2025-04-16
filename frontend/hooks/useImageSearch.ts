import { useState, useEffect, useRef } from 'react';
import BASE_URL from '../utils/config';

export interface UnsplashImage {
  id: string;
  url: string;
  alt_description: string;
}

export const useImageSearch = () => {
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

  const [title, setTitle] = useState('');

  const scrollContainerRef = useRef<HTMLDivElement | null>(null);
  const modalRef = useRef<HTMLDivElement | null>(null);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleImageSelect = (url: string) => {
    setTempSelectedImageUrl(url);
  };

  // Funktion, um den Titel zu setzen
  const updateTitle = (newTitle: string) => {
    setTitle(newTitle); // Titel setzen
    if (!imageSearchTerm) {
      setImageSearchTerm(newTitle); // Nur setzen, wenn imageSearchTerm noch leer ist
    }
  };

   // Falls der title sich ändert, den imageSearchTerm setzen
   useEffect(() => {
    if (!imageSearchTerm) {
      setImageSearchTerm(title); // Nur setzen, wenn imageSearchTerm noch leer ist
    }
  }, [title, imageSearchTerm]); // Titel wird überwacht

  // Synchronise fields for 'title' and 'image'
    useEffect(() => {
      if (!hasManuallyEditedSearch) {
        setImageSearchTerm(title);
      }
    }, [title, hasManuallyEditedSearch]);

  const handleConfirmSelection = () => {
    if (tempSelectedImageUrl) {
      setSelectedImageUrl(tempSelectedImageUrl);
      setTempSelectedImageUrl(null);
      setIsModalOpen(false);
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement, UIEvent>) => {
    const bottom = e.currentTarget.scrollHeight === e.currentTarget.scrollTop + e.currentTarget.clientHeight;
    setIsAtBottom(bottom); // Wenn das Ende erreicht ist, setzen wir isAtBottom auf true
  };

  const searchImages = async () => {
    if (!imageSearchTerm) return;
    setIsSearching(true);
    setCurrentPage(1);
    try {
      const response = await fetch(`${BASE_URL}/search-images?query=${encodeURIComponent(imageSearchTerm)}&page=1`);
      const data = await response.json();
      setImageResults(data.results);
      setIsModalOpen(true);
    } catch (err) {
      console.error('Fehler bei der Bildsuche:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const loadMoreImages = async () => {
    if (loadingMore) return;
    setLoadingMore(true);
    setIsAtBottom(false);

    const nextPage = currentPage + 1;

    try {
      const response = await fetch(`${BASE_URL}/search-images?query=${encodeURIComponent(imageSearchTerm)}&page=${nextPage}`);
      const data = await response.json();
      setImageResults((prev) => [...prev, ...data.results]);
      setCurrentPage(nextPage);
    } catch (err) {
      console.error('Fehler beim Nachladen:', err);
    } finally {
      setLoadingMore(false);
    }
  };

  return {
    imageSearchTerm,
    setImageSearchTerm,
    selectedImageUrl,
    tempSelectedImageUrl,
    setSelectedImageUrl,
    setTempSelectedImageUrl,
    isModalOpen,
    openModal,
    closeModal,
    handleScroll,
    hasManuallyEditedSearch,
    setHasManuallyEditedSearch,
    searchImages,
    handleImageSelect,
    handleConfirmSelection,
    imageResults,
    isSearching,
    loadMoreImages,
    isAtBottom,
    updateTitle,
    loadingMore,
    scrollContainerRef,
    modalRef,
  };
};