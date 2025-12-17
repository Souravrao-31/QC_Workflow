import { api } from "./client";

export interface Drawing {
  id: string;
  status: string;
  assigned_to: string | null;
  assigned_to_name?: string | null;
  title: string
}

export type AuditLog = {
  id: string;
  drawing_title: string;
  user_name: string;
  action: string;
  from_status: string | null;
  to_status: string | null;
  created_at: string;
};
export async function fetchDrawings(): Promise<Drawing[]> {
  const response = await api.get<Drawing[]>("/drawings");
  return response.data;
}

export async function fetchAudit(): Promise<AuditLog[]> {
  const response = await api.get<AuditLog[]>("/audit");
  return response.data;
}

export async function fetchMyDrawings(): Promise<Drawing[]> {
  const response = await api.get<Drawing[]>("/drawings/me");
  return response.data;
}

export async function performDrawingRelease(id: string) {
  return api.post(`/drawings/${id}/release`);
}

export async function performDrawingAction(
  drawingId: string,
  action: "CLAIM" | "SUBMIT" | "APPROVE" | "ASSIGN"
) {
  await api.post(`/drawings/${drawingId}/actions`, {
    action,
  });
}