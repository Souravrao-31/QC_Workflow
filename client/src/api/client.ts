import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI base URL
  headers: {
    "Content-Type": "application/json",
  },
});
