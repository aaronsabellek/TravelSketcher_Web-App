import Link from "next/link";

// Footer of website
const Footer = () => {
  return (
    <footer className="bg-gray-100 border-t border-b border-gray-300 mt-8">
      <div className="max-w-7xl mx-auto px-4 py-6 text-sm text-gray-600 flex justify-between">
        <p>&copy; {new Date().getFullYear()} TravelSketcher</p>
        <div className="space-x-4">

          {/* Privacy Policy */}
          <Link
            href="/privacy_policy"
            className="hover:underline cursor-pointer"
          >
            Privacy policy
          </Link>

          {/* Terms and conditions */}
          <Link
            href="terms_and_conditions"
            className="hover:underline cursor-pointer"
          >
            Terms and conditions
          </Link>

        </div>
      </div>
    </footer>
  );
};

  export default Footer;