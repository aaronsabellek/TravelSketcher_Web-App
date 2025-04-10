

const Footer = () => {
  return (
    <footer className="bg-gray-100 border-t border-gray-300 mt-8">
      <div className="max-w-7xl mx-auto px-4 py-6 text-sm text-gray-600 flex justify-between">
        <p>&copy; {new Date().getFullYear()} MyTravelSite</p>
        <div className="space-x-4">
          <a href="/privacy" className="hover:underline">Datenschutz</a>
          <a href="/terms" className="hover:underline">AGB</a>
        </div>
      </div>
    </footer>
  );
};

  export default Footer;