import { AppProps } from 'next/app';
import { AuthProvider } from '../contexts/AuthContext';
import Layout from '../components/Layout';
import '../styles/globals.css';
import '../styles/navbar.css';
import '../styles/footer.css';
import '../styles/layout.css';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}