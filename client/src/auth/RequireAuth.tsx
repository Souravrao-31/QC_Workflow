import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

export type UserRole = "ADMIN" | "DRAFTER" | "SHIFT_LEAD" | "FINAL_QC";

export interface AuthUser {
  id: string;
  role: UserRole;
}

interface AuthContextType {
  user: AuthUser;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();

  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("qc_access_token");

    if (!token) {
      navigate("/");
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));

      setUser({
        id: payload.sub,
        role: payload.role,
      });

      api.defaults.headers.common.Authorization = `Bearer ${token}`;
    } catch {
      localStorage.removeItem("qc_access_token");
      navigate("/");
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  if (loading) {
    return null; // or spinner
  }

  if (!user) {
    return null;
  }

  return (
    <AuthContext.Provider value={{ user, logout }}>
      {children}
    </AuthContext.Provider>
  );

  function logout() {
    localStorage.removeItem("qc_access_token");
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
