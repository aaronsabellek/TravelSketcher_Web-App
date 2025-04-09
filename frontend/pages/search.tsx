import React from 'react';
import { useRedirectIfNotAuthenticated } from '../utils/authRedirects';

const Search = () => {

  // Redirect user if not authenticated
  useRedirectIfNotAuthenticated();

  return (
    <div>
      <h1>Search</h1>
      <p>
      Search..
      </p>
    </div>
  );
};

export default Search;