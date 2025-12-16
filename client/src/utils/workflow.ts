export type Role =
  | "ADMIN"
  | "DRAFTER"
  | "SHIFT_LEAD"
  | "FINAL_QC";

export function getAvailableActions(
  role: Role,
  status: string,
  isAssignedToMe: boolean
): ("CLAIM" | "SUBMIT" | "APPROVE")[] {
  if (status === "UNASSIGNED" && role === "ADMIN") {
    return ["CLAIM"];
  }

  if (status === "DRAFTING" && role === "DRAFTER") {
    return isAssignedToMe ? ["SUBMIT"] : ["CLAIM"];
  }

  if (status === "FIRST_QC" && role === "SHIFT_LEAD") {
    return isAssignedToMe ? ["SUBMIT"] : ["CLAIM"];
  }

  if (status === "FINAL_QC" && role === "FINAL_QC") {
    return isAssignedToMe ? ["APPROVE"] : ["CLAIM"];
  }

  return [];
}
