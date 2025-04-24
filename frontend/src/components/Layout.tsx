import { ReactNode } from 'react';
import { Toaster } from 'sonner';

import Navbar from './Navbar';
import Footer from './Footer';

const Layout = ({ children }: { children: ReactNode }) => {
    return (
      <div>
        <Navbar />
          <main className="max-w-6xl mx-auto px-3">
            <Toaster position="top-right" />
            {children}
          </main>
        <Footer />
      </div>
    );
  };

  export default Layout;