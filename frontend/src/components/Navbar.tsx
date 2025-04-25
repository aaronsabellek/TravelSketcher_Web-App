import Link from 'next/link';
import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion'

import { useAuth } from '@/contexts/AuthContext';
import { useClickOutside } from '@/hooks/useClickOutside';
import Button from './Buttons/Button';

const Navbar = () => {

  const { isLoggedIn, logout, isLoading } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Hook to close Burger Menu by clicking outside menu
  useClickOutside([menuRef, buttonRef], () => setMenuOpen(false), menuOpen);

  // Links for logged in user
  const loggedInLinks = [
    { href: '/destination/get_all', label: 'Destinations' },
    { href: '/user/profile', label: 'Profile' },
  ];

  // Links not logged in
  const loggedOutLinks = [
    { href: '/about', label: 'About' },
    { href: '/register', label: 'Registration' }
  ];

  const menuLinks = isLoggedIn ? loggedInLinks : loggedOutLinks;

  // Menu visibility for effect
  const menuVariants = {
    hidden: {
      opacity: 0,
      height: 0,
      transition: { duration: 0.3, ease: 'easeOut' },
    },
    visible: {
      opacity: 1,
      height: 'auto',
      transition: { duration: 0.3, ease: 'easeOut' },
    },
  };

  // Open/close burger menu
  const toggleMenu = () => setMenuOpen(prev => !prev);
  const handleLinkClick = () => setMenuOpen(false);

  // Loading
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <nav className="bg-white">
      <div className="max-w-7xl mx-auto px-4 mb-2">
        <div className="flex flex-wrap justify-between items-center h-16">

          {/* Logo / Title */}
          <div className="flex-shrink-0 text-gray-800 font-bold text-xl">
            <Link href="/">TravelSketcher</Link>
          </div>

          {/* Burger-Icon for small screens */}
          <div className="md:hidden">
            <motion.button
              ref={buttonRef}
              onClick={toggleMenu}
              className="focus:outline-none"
              aria-label="Toggle menu"
              aria-expanded={menuOpen}
              animate={{ rotate: menuOpen ? -90 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <img
                src="/burger_menu_icon.png"
                alt="Menu"
                className="h-6 w-6"
              />
            </motion.button>
          </div>

          {/* Navigation for desktop screens */}
          <div className="hidden md:flex flex items-center space-x-6 text-gray-700 font-medium">
            {(isLoggedIn ? loggedInLinks : loggedOutLinks).map((link) => (
              <Link key={link.href} href={link.href} className="hover:underline">
                {link.label}
              </Link>
            ))}

            {!isLoggedIn ? (
              <Link href="/login">
                <Button
                  text="Login"
                  onClick={handleLinkClick}
                  type="button"
                />
              </Link>
            ): (
              <Button
                text="Logout"
                onClick={logout}
                type="button"
              />
            )}

          </div>
        </div>

        {/* Animated Mobile Menu */}
        <AnimatePresence>
          {menuOpen && (
            <motion.div
              ref={menuRef}
              initial="hidden"
              animate="visible"
              exit="hidden"
              variants={menuVariants}
              className="md:hidden overflow-hidden"
            >
              <div className="mt-2 space-y-2 text-gray-700 font-medium">
              {menuLinks.map(link => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="block px-2 py-1 hover:underline"
                    onClick={handleLinkClick}
                  >
                    {link.label}
                  </Link>
                ))}

                {!isLoggedIn ? (
                  <Link href="/login">
                    <Button
                      text="Login"
                      type="button"
                      onClick={handleLinkClick}
                    />
                  </Link>
                ) : (
                  <Button
                    text="Logout"
                    onClick={() => {
                      logout();
                      handleLinkClick();
                    }}
                    type="button"
                  />
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  );
};

export default Navbar;