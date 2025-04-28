import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner';

// 404 page
const Custom404 = () => {
  const router = useRouter();

  useEffect(() => {

    toast.error('This page does not exist. You will be redirected to the homepage.');

    // Redirect to homepage after 3 seconds
    setTimeout(() => {
      router.push('/');
    }, 3000);
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p className="text-center text-xl">Page not found. You will be redirected to the homepage.</p>
    </div>
  );
};

export default Custom404;