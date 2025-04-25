import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'sonner'; // Oder eine andere Toast-Bibliothek, die du verwendest

const Custom404 = () => {
  const router = useRouter();

  useEffect(() => {
    // Zeige einen Toast an, dass die Seite nicht gefunden wurde
    toast.error('Diese Seite existiert nicht. Du wirst zur Startseite weitergeleitet.');

    // Leite nach 3 Sekunden zur Startseite weiter
    setTimeout(() => {
      router.push('/');
    }, 3000);
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p className="text-center text-xl">Seite nicht gefunden. Du wirst zur Startseite weitergeleitet.</p>
    </div>
  );
};

export default Custom404;