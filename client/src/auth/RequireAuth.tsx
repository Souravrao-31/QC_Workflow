import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";


export type UserRole =
  | "ADMIN"
  | "DRAFTER"
  | "SHIFT_LEAD"
  | "FINAL_QC";

export interface AuthUser {
  id: string;
  role: UserRole;
}


interface AuthContextType {
  user: AuthUser;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);


export function RequireAuth({
  children,
}: {
  children: React.ReactNode;
}) {
  const navigate = useNavigate();
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/");
      return;
    }

    // Decode payload safely
    const payload = JSON.parse(
      atob(token.split(".")[1])
    );

    setUser({
      id: payload.sub,
      role: payload.role,
    });

    // Attach token to axios
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  }, [navigate]);

  if (!user) {
    return null; // Or loading spinner
  }

  return (
    <AuthContext.Provider value={{ user, logout }}>
      {children}
    </AuthContext.Provider>
  );

  function logout() {
    localStorage.removeItem("access_token");
    navigate("/");
  }
}


export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside RequireAuth");
  }
  return ctx;
}
