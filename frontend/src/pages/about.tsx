import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { AnimatePresence, motion } from 'framer-motion';

import { useRedirectIfAuthenticated } from '@/hooks/authRedirects';

const About = () => {
  // Redirect if user is authenticated
  const { isReady } = useRedirectIfAuthenticated();

  const [isAreaHovered, setIsAreaHovered] = useState(false);
  const [hoveredImageIndex, setHoveredImageIndex] = useState<number | null>(null);
  const [, setIsButtonHovered] = useState(false);
  const [imagesLoaded, setImagesLoaded] = useState([false, false, false]);

  const showButton = isAreaHovered;

  // Load images
  useEffect(() => {
    const imageUrls = ['/travel-img-1.png', '/travel-img-2.png', '/travel-img-3.png'];

    imageUrls.forEach((url, index) => {
      const img = new Image();
      img.src = url;
      img.onload = () => {
        setImagesLoaded((prev) => {
          const updated = [...prev];
          updated[index] = true;
          return updated;
        });
      };
    });
  }, []);

  const allImagesLoaded = imagesLoaded.every(Boolean);

  // Wait until authentication state is ready
  if (!isReady) return null;

  return (
    <div>
      <div
        className="relative"
        onMouseEnter={() => setIsAreaHovered(true)}
        onMouseLeave={() => {
          setIsAreaHovered(false);
          setHoveredImageIndex(null);
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none ">
          <div className="pointer-events-auto transition-opacity duration-500 flex flex-col items-center justify-center text-center">
            <AnimatePresence mode="wait">
              {showButton ? (

                // when user hovers
                <motion.div
                  key="with-button"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="flex flex-col items-center"
                >
                  <h2 className="text-white mb-4 text-3xl sm:text-4xl md:text-5xl font-extrabold text-center transition-colors duration-500 drop-shadow-lg">
                    Register and find out:
                  </h2>
                  <Link href="/register">
                    <button
                      className="border-2 mt-4 cursor-pointer border-white text-white px-6 py-3 text-lg font-semibold rounded-lg transition-all duration-300 hover:bg-white hover:text-black"
                      onMouseEnter={() => setIsButtonHovered(true)}
                      onMouseLeave={() => setIsButtonHovered(false)}
                    >
                      Register
                    </button>
                  </Link>
                </motion.div>
              ) : (

                // when user does not hover
                <motion.h2
                  key="without-button"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="text-white text-3xl sm:text-4xl md:text-5xl font-extrabold text-center drop-shadow-lg"
                >
                  Which adventure awaits you?
                </motion.h2>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Image Gallery */}
        {allImagesLoaded ? (
          <div className="flex justify-between -mx-3 max-h-100 mt-3 sm:max-h-full sm:mt-0">
            {[1, 2, 3].map((num, index) => {
              const isHovered = hoveredImageIndex === index;
              const brightness =
                isHovered ? 'brightness-75' : index === 1 ? 'brightness-100' : 'brightness-90';

              return (
                <div
                  key={num}
                  className="relative flex-1 min-w-0 overflow-hidden"
                  onMouseEnter={() => setHoveredImageIndex(index)}
                  onMouseLeave={() => setHoveredImageIndex(null)}
                >
                  <div
                    className={`
                      bg-cover bg-center
                      ${brightness}
                      ${isHovered ? 'scale-105' : ''}
                      transition-all duration-500 w-full h-[500px]
                    `}
                    style={{
                      backgroundImage: `url(/travel-img-${num}.png)`,
                    }}
                  />
                </div>
              );
            })}
          </div>
        ) : (
          <div className="h-[500px] w-full flex items-center justify-center">
            <span className="text-white text-lg">Loading...</span>
          </div>
        )}
      </div>

      {/* About Text */}
      <div className="w-full my-10">
        <div className="max-w-5xl mx-auto px-4">
          <h1 className="text-3xl font-extrabold text-center mb-8">About This Project</h1>

          <p className="about">
            <b>TravelSketcher</b> is your personal space to capture and organize your travel dreams — simply and beautifully.
          </p>

          <p className="about">
            Instead of overwhelming you with offers and complex planning tools, TravelSketcher focuses on what truly matters: your destinations, your activities, and your memories.
          </p>

          <p className="about">
            Save your favorite places, plan activities, add notes, and tag important details — all in one clean and intuitive view.
          </p>

          <p className="about">
            With stunning Unsplash images integrated into your plans, every trip you imagine feels vivid and inspiring even before you set foot on the road.
          </p>

          <p className="about">
            TravelSketcher is about simplicity, creativity, and keeping your travel dreams close at hand.
          </p>

          <p className="about">
            Start sketching your next adventure today.
          </p>

        </div>
      </div>
    </div>
  );
};

export default About;