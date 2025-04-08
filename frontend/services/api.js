const BASE_URL = 'http://localhost:5000';

// Login-Funktion
export async function login(email, password) {
    const res = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // <- wichtig für Cookie
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) throw new Error("Login fehlgeschlagen");

    const data = await res.json();
    if (data.message === 'Login successful!') {
      return data; // Gibt eine Erfolgsnachricht zurück, die du für Tests verwenden kannst
    } else {
      throw new Error("Unbekannter Fehler beim Login");
    }
  }