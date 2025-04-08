// pages/login.js
import { useState } from "react";
import { login, getUserProfile } from "../services/api";
import { useRouter } from "next/router";

export default function LoginPage() {
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("1234");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const loginResponse = await login(email, password);  // Login durchführen und Antwort holen
      console.log("Login Response:", loginResponse.message);  // Erfolgsnachricht anzeigen

      if (loginResponse.message === 'Login successful!') {
        // Erfolgsnachricht prüfen
        router.push("/"); // Weiterleitung zur Startseite oder einer anderen geschützten Seite
      } else {
        setError("Login fehlgeschlagen"); // Wenn die Nachricht nicht 'Login successful!' ist
      }
    } catch (err) {
      setError(err.message || "Login fehlgeschlagen");  // Zeigt die Fehlermeldung an
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form onSubmit={handleLogin} className="space-y-3">
        <input
          type="email"
          placeholder="E-Mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 w-full"
        />
        <input
          type="password"
          placeholder="Passwort"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 w-full"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Einloggen
        </button>
      </form>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}