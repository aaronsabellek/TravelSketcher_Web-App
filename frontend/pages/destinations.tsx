import React from 'react';
import { useRedirectIfNotAuthenticated } from '../utils/authRedirects';

const Destinations = () => {

  // Redirect user if not authenticated
  useRedirectIfNotAuthenticated();

  return (
    <div>
      <h1>Destinations</h1>
      <p>
        Destinations..
      </p>
    </div>
  );
};

export default Destinations;