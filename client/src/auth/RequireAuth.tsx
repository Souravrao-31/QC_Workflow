import { Navigate } from "react-router-dom";
import { getToken } from "../api/authStorage";
import type { JSX } from "react";

export default function RequireAuth({ children }: { children: JSX.Element }) {
  const token = getToken();

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return children;
}
