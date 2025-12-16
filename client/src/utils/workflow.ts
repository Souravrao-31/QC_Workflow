export type Role =
  | "ADMIN"
  | "DRAFTER"
  | "SHIFT_LEAD"
  | "FINAL_QC";

export type Action = "ASSIGN" | "CLAIM" | "SUBMIT" | "APPROVE";

export function getAvailableActions(
  role: Role,
  status: string,
  isAssignedToMe: boolean
): Action[] {
  // UNASSIGNED → only ADMIN can ASSIGN
  if (status === "UNASSIGNED" && role === "ADMIN") {
    return ["ASSIGN"];
  }

  // DRAFTING
  if (status === "DRAFTING" && role === "DRAFTER") {
    return isAssignedToMe ? ["SUBMIT"] : ["CLAIM"];
  }

  // FIRST QC
  if (status === "FIRST_QC" && role === "SHIFT_LEAD") {
    return isAssignedToMe ? ["SUBMIT"] : ["CLAIM"];
  }

  // FINAL QC
  if (status === "FINAL_QC" && role === "FINAL_QC") {
    return isAssignedToMe ? ["APPROVE"] : ["CLAIM"];
  }

  return [];
}
