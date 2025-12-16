import { api } from "./client";

export interface Drawing {
  id: string;
  status: string;
  assigned_to: string | null;
  assigned_to_name?: string | null;
}

export async function fetchDrawings(): Promise<Drawing[]> {
  const response = await api.get<Drawing[]>("/drawings");
  return response.data;
}
