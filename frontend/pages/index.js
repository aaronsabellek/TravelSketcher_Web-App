import { logout } from "../services/api";

const handleLogout = async () => {
  try {
    await logout();
    alert("Ausgeloggt!");
  } catch (err) {
    console.error("Logout fehlgeschlagen", err);
  }
};