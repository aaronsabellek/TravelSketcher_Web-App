import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

const Navbar = () => {
  const { isLoggedIn, logout, isLoading } = useAuth();

  // Ladezustand berücksichtigen
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <nav className="bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">

          {/* Logo / Titel */}
          <div className="flex-shrink-0 text-gray-800 font-bold text-xl">
            <Link href="/">TravelSketcher</Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6 text-gray-700 font-medium">
            {isLoggedIn ? (
              <>
                <Link href="/destination/get_all" className="hover:underline">Destinations</Link>
                <Link href="/search" className="hover:underline">Search</Link>
                <Link href="/user/profile" className="hover:underline">Profile</Link>
                <button
                  onClick={logout}
                  className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/about" className="hover:underline">About</Link>
                <Link href="/register" className="hover:underline">Registration</Link>
                <Link href="/login">
                  <span className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition">
                    Login
                  </span>
                </Link>
              </>
            )}
          </div>
          {/* empty block for centering */}
          <div className="inline-block">
          </div>
        </div>

      </div>
    </nav>
  );
};

export default Navbar;