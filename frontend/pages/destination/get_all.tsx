import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import { useRedirectIfNotAuthenticated } from '../../utils/authRedirects';
import Link from 'next/link';
import BASE_URL from '../../utils/config';

interface Destination {
  id: string;
  img_link: string;
  title: string;
  country: string;
  status: string;
  tags: string;
  duration: string;
  time: string;
  pricing: string;
  travel_duration_flight: string;
  trip_pricing_flight: string;
}

const DestinationsPage = () => {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useRedirectIfNotAuthenticated();

  // Funktion zum Abrufen der Destinations
  const fetchDestinations = async () => {
    try {
      const response = await fetch(`${BASE_URL}/destination/get_all`, {
        credentials: 'include',
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Hier könntest du eventuell noch einen Authentifizierungsheader hinzufügen, wenn nötig
          // 'Authorization': `Bearer ${token}`
        },
      });

      if (!response.ok) {
        throw new Error('Fehler beim Laden der Destinations');
      }

      const data = await response.json();
      console.log('API Response:', data); // Antwort loggen

      if (data.destinations) {
        setDestinations(data.destinations);
      }
    } catch (err) {
      console.error('Error fetching destinations:', err);
      setError('Fehler beim Laden der Destinations');
    } finally {
      setLoading(false);
    }
  };

  // Effekt, um die Destinations beim Laden der Seite abzurufen
  useEffect(() => {
    fetchDestinations();
  }, []);

  // Handler für Bearbeiten und Löschen (je nach Funktionalität)
  const handleEdit = (id: string) => {
    // Logik für Bearbeiten
    router.push(`/edit-destination/${id}`);
  };

  const handleDelete = async (id: string) => {
    try {
      await axios.delete(`/destination/delete/${id}`);
      setDestinations(destinations.filter((dest) => dest.id !== id));
    } catch (err) {
      setError('Fehler beim Löschen der Destination');
    }
  };

  return (
    <div className="container max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">My Destinations</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 hover:">
        {destinations.map((destination) => (
        <Link href="/user/profile">
          <div key={destination.id} className="bg-white hover:brightness-95 rounded-lg pb-2">
            <div className="relative aspect-[16/12] w-full rounded-lg overflow-hidden">
              <img
                src='/travel-img-2.png'
                alt={destination.title}
                className="w-full h-full object-cover hover:brightness-75 hover:scale-105 transition-all duration-500"
              />
              <div className="absolute top-2 right-2 text-white">
                <button onClick={() => handleEdit(destination.id)} className="text-xl">⋮</button>
                <button onClick={() => handleDelete(destination.id)} className="ml-2 text-xl">❌</button>
              </div>
            </div>
            <div className="">
              <div className="flex p-2">
                <div className="mr-5">
                    <h2 className="text-xl font-semibold">{destination.title}</h2>
                    <p className="text-sm text-gray-500">{destination.country}</p>
                </div>
                <h2 className="mt-2 text-base text-white bg-blue-500 pt-2 px-3 rounded-2xl">{destination.status}</h2>
              </div>

              <p className="hidden  mt-2 text-lg">{destination.tags}</p>

              {/* Nach rechts wischbarer Bereich */}
              <div className="mt-4 hidden p-4 border shadow-md border-gray-300 bg-gray-300/25">
                <div className="flex space-x-4">
                  <div>
                    <p>⏰: {destination.duration}</p>
                    <p>📅: {destination.time}</p>
                    <p>💸: {destination.pricing}</p>
                    <p>✈️: {destination.travel_duration_flight}, {destination.trip_pricing_flight}</p>
                  </div>
                </div>
              </div>

              {/* Symbole für Google-Suche, Notizen und Rome2Rio */}
              <div className="hidden mt-4 flex justify-end space-x-4">
                <button
                  onClick={() =>
                    window.open(`https://www.google.com/search?q=${destination.title} ${destination.country}`, '_blank')
                  }
                  className="text-blue-500 hover:text-blue-700"
                >
                  🔍
                </button>
                <button
                  onClick={() => alert('Freitext Notizen anzeigen')} // Logik für Notizen einfügen
                  className="text-green-500 hover:text-green-700"
                >
                  📝
                </button>
                <button
                  onClick={() =>
                    window.open(`https://www.rome2rio.com/map/${destination.country} to ${destination.title}`, '_blank')
                  }
                  className="text-orange-500 hover:text-orange-700"
                >
                  🚗
                </button>
              </div>
            </div>
          </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default DestinationsPage;