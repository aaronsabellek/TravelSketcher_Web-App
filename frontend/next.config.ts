import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export',  // Stellt den statischen Export ein
  images: {
    unoptimized: true, // Optional, falls du externe Bilder ohne Optimierung verwenden möchtest
  },
};

export default nextConfig;
