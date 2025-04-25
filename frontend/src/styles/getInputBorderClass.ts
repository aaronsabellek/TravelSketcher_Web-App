export const getInputBorderClass = (value: string, errors: string[]): string => {
    // Wenn das Eingabefeld leer ist, eine neutrale Umrandung anzeigen
    if (value.trim() === '') {
      return 'border-gray-300 focus:border-gray-500 focus:ring-gray-500'; // Leeres Feld - neutrale Umrandung
    }

    // Wenn Fehler vorhanden sind, rote Umrandung
    if (errors.length > 0) {
      return 'border-red-500 focus:border-red-500 focus:ring-red-500'; // Fehler vorhanden
    }

    // Wenn keine Fehler vorliegen, grüne Umrandung
    return 'border-blue-500 focus:border-blue-500 focus:ring-blue-500'; // Keine Fehler
  };