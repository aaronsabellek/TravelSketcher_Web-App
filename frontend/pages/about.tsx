import React from 'react';

const About = () => {
  return (
    <div>
      <div className="">
      <div className="relative w-full max-w-7xl mx-auto py-20 px-4">
        {/* Overlay Text */}
        <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
          <h2 className="text-white group-hover:text-gray-900 text-3xl sm:text-4xl md:text-5xl font-extrabold text-center transition-colors duration-500 drop-shadow-lg">
            Which adventure waits for you?
          </h2>
        </div>

        {/* Image Gallery */}
        <div className="flex justify-between">
          {/* Image 1 */}
          <div className="group relative flex-1 min-w-0 overflow-hidden">
            <div
              className="bg-cover bg-center brightness-90 group-hover:brightness-75 transform group-hover:scale-105 transition-all duration-500 rounded-l-xl"
              style={{
                backgroundImage: `url(/travel-img-1.png)`,
                height: '400px', // Höhe der Bilder
              }}
            />
          </div>

          {/* Image 2 */}
          <div className="group relative flex-1 min-w-0 overflow-hidden">
            <div
              className="bg-cover bg-center brightness-100 group-hover:brightness-75 transform group-hover:scale-105 transition-all duration-500"
              style={{
                backgroundImage: `url(/travel-img-3.png)`,
                height: '400px', // Höhe der Bilder
              }}
            />
          </div>

          {/* Image 3 */}
          <div className="group relative flex-1 min-w-0 overflow-hidden">
            <div
              className="bg-cover bg-center brightness-90 group-hover:brightness-75 transform group-hover:scale-105 transition-all duration-500 rounded-r-xl"
              style={{
                backgroundImage: `url(/travel-img-2.png)`,
                height: '400px', // Höhe der Bilder
              }}
            />
          </div>
        </div>
        </div>
      </div>

      <div className="mb-20">
        <div className="max-w-5xl mx-auto px-4">
          <h1 className="text-3xl font-extrabold text-center mb-8">About This Project</h1>
          <p className="text-lg mb-8">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur non feugiat purus.
            Nulla facilisi. Morbi imperdiet, nisl nec fringilla accumsan, lorem risus feugiat nisl,
            nec egestas neque erat ut justo. Sed volutpat, sapien non tincidunt pulvinar, velit nunc
            mattis sapien, id gravida leo erat sed justo. Duis id nisl non metus ultrices placerat.
          </p>
          <p className="text-lg">
            Vestibulum in varius quam. Pellentesque sagittis porttitor sapien, vel dapibus magna
            blandit non. Integer cursus eros at facilisis hendrerit. Donec bibendum lacus sit amet
            fermentum fringilla. Praesent semper leo vitae velit mattis, at hendrerit lacus maximus.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;