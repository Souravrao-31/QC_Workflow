import { api } from "./client";

export interface Drawing {
  id: string;
  status: string;
  assigned_to: string | null;
  assigned_to_name?: string | null;
  title: string
}

export async function fetchDrawings(): Promise<Drawing[]> {
  const response = await api.get<Drawing[]>("/drawings");
  return response.data;
}

export async function fetchMyDrawings(): Promise<Drawing[]> {
  const response = await api.get<Drawing[]>("/drawings/me");
  return response.data;
}


export async function performDrawingAction(
  drawingId: string,
  action: "CLAIM" | "SUBMIT" | "APPROVE" | "ASSIGN"
) {
  await api.post(`/drawings/${drawingId}/actions`, {
    action,
  });
}