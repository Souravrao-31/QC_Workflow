import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Button,
  Box,
} from "@chakra-ui/react";
import { getAvailableActions } from "../utils/workflow";

const statusColor = (status: string) => {
  switch (status) {
    case "UNASSIGNED":
      return "gray";
    case "DRAFTING":
      return "blue";
    case "FIRST_QC":
      return "orange";
    case "FINAL_QC":
      return "purple";
    case "APPROVED":
      return "green";
    default:
      return "gray";
  }
};

export default function DrawingsTableView({
  drawings,
  user,
  onAction,
  onRelease,
}: any) {
  return (
    <Box bg="white" p={4} rounded="md" shadow="sm">
      <Table>
        <Thead>
          <Tr>
            <Th>Drawing</Th>
            <Th>Status</Th>
            <Th>Assigned To</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>

        <Tbody>
          {drawings.map((d: any) => (
            <Tr key={d.id}>
              <Td>{d.title}</Td>
              <Td>
                <Badge colorScheme={statusColor(d.status)}>{d.status}</Badge>
              </Td>
              <Td>{d.assigned_to_name ?? "—"}</Td>
              <Td>
                {getAvailableActions(
                  user.role,
                  d.status,
                  d.assigned_to === user.id
                ).map((action: string) => (
                  <Button
                    key={action}
                    size="sm"
                    mr={2}
                    onClick={() => onAction(d.id, action)}
                  >
                    {action}
                  </Button>
                ))}
              </Td>

              {d.assigned_to === user.id &&
                d.status !== "APPROVED" &&
                onRelease && (
                  <Button
                    size="sm"
                    colorScheme="red"
                    variant="outline"
                    onClick={() => onRelease(d.id)}
                  >
                    Release
                  </Button>
                )}
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}
