import { useState, useEffect, useRef, useCallback } from 'react';
import { BASE_URL } from '../utils/config';
import { UnsplashImage } from '../types/models';

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

  const loadMoreImages = useCallback(async () => {
    if (loadingMore) return;

    setLoadingMore(true);
    setIsAtBottom(false);

    try {
      const res = await fetch(`${BASE_URL}/search-images?query=${encodeURIComponent(imageSearchTerm)}&page=${currentPage + 1}`);
      const data = res.ok ? await res.json() : null;

      if (data?.results?.length) {
        setImageResults((prev) => [...prev, ...data.results]);
        setCurrentPage((p) => p + 1);
      }
    } finally {
      setLoadingMore(false);
    }
  }, [loadingMore, imageSearchTerm, currentPage]);


  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement, UIEvent>) => {
    const container = e.currentTarget;
    const bottom = container.scrollHeight - container.scrollTop === container.clientHeight;

    if (bottom && !loadingMore) {
      loadMoreImages();
    }
  }, [loadingMore, loadMoreImages]);


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
    hasManuallyEditedSearch,
    setHasManuallyEditedSearch,
    searchImages,
    handleImageSelect,
    handleConfirmSelection,
    handleScroll,
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