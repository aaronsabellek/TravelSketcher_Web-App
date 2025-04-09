import Navbar from './Navbar';
import Footer from './Footer';

const Layout = ({ children }: { children: React.ReactNode }) => {
    return (
      <div className="layout-wrapper">
          <Navbar />
          <main className="content">
            {children}
          </main>
          <Footer />
      </div>
    );
  };

  export default Layout;