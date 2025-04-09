import { useAuth } from '../contexts/AuthContext';
import Link from 'next/link';

const Navbar = () => {
  const { isLoggedIn, logout, isLoading } = useAuth();

  // Ladezustand berücksichtigen
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <nav className="navbar">
      <ul>
        <li><Link href="/about">About</Link></li>
        {isLoggedIn ? (
          <>
            <li><Link href="/destinations">Destinations</Link></li>
            <li><Link href="/search">Search</Link></li>
            <li><Link href="/user/profile">Profile</Link></li>
            <li><button onClick={logout} className="logout-button">Logout</button></li>
          </>
        ) : (
          <>
            <li><Link href="/register">Registration</Link></li>
            <li><Link href="/login">Login</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;