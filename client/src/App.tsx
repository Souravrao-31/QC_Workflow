import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./auth/LoginPage";
import DashboardPage from "./dashboard/DashboardPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  );
}
