import axios from "axios";
import { getToken } from "../api/authStorage";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

//  Attach JWT automatically
api.interceptors.request.use((config) => {
  const token = getToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("qc_access_token");
      window.location.href = "/";
    }
    return Promise.reject(error);
  }
);
