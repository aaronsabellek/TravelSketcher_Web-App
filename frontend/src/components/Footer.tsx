// Footer of website
const Footer = () => {
  return (
    <footer className="bg-gray-100 border-t border-b border-gray-300 mt-8">
      <div className="max-w-7xl mx-auto px-4 py-6 text-sm text-gray-600 flex justify-between">
        <p>&copy; {new Date().getFullYear()} TravelSketcher</p>
        <div className="space-x-4">
          <a href="/privacy" className="hover:underline">Privacy policy</a>
          <a href="/terms" className="hover:underline">Terms and conditions</a>
        </div>
      </div>
    </footer>
  );
};

  export default Footer;