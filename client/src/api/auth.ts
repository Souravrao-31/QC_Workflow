import { api } from "./client";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(name: string, password: string) {
  const response = await api.post<LoginResponse>("/login", {
    name,
    password,
  });

  return response.data;
}
