import React, { useState } from 'react';
import { useRedirectIfAuthenticated } from '../utils/authRedirects';
import Link from 'next/link';

const About = () => {
  const [isAreaHovered, setIsAreaHovered] = useState(false);
  const [hoveredImageIndex, setHoveredImageIndex] = useState<number | null>(null);
  const [isButtonHovered, setIsButtonHovered] = useState(false);

  const showButton = isAreaHovered;

  // Redirect if user is authenticated
  useRedirectIfAuthenticated();

  return (
    <div>
      <div
        className="relative w-full max-w-7xl mx-auto"
        onMouseEnter={() => setIsAreaHovered(true)}
        onMouseLeave={() => {
          setIsAreaHovered(false);
          setHoveredImageIndex(null);
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
          <div className="pointer-events-auto transition-opacity duration-500 flex flex-col items-center justify-center text-center">
            {showButton ? (
              <div>
              <h2 className="text-white mb-4 text-3xl sm:text-4xl md:text-5xl font-extrabold text-center transition-colors duration-500 drop-shadow-lg">
                Register and find out:
              </h2>
              <Link href="/register">
                <button
                  className="border-2 mt-4 border-white text-white px-6 py-3 text-lg font-semibold rounded-lg transition-all duration-300 hover:bg-white hover:text-black"
                  onMouseEnter={() => setIsButtonHovered(true)}
                  onMouseLeave={() => setIsButtonHovered(false)}
                >
                  Register
                </button>
              </Link>
              </div>
            ) : (
              <h2 className="text-white text-3xl sm:text-4xl md:text-5xl font-extrabold text-center transition-colors duration-500 drop-shadow-lg">
                Which adventure awaits you?
              </h2>
            )}
          </div>
        </div>

        {/* Image Gallery */}
        <div className="flex justify-between">
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
      </div>

      {/* About Text */}
      <div className="w-full mt-20 mb-20">
        <div className="max-w-5xl mx-auto px-4">
          <h1 className="text-3xl font-extrabold text-center mb-8">About This Project</h1>
          <p className="text-lg mb-8">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
          sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem
          ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore
          magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
          sanctus est Lorem ipsum dolor sit amet.
          </p>
          <p className="text-lg">
          Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at
          vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.
          Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;