import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Box,
  Text,
} from "@chakra-ui/react";
import { type AuditLog } from "../api/drawings";

const actionColor = (action: string) => {
  switch (action) {
    case "CLAIM":
      return "blue";
    case "SUBMIT":
      return "orange";
    case "APPROVE":
      return "green";
    case "RELEASE":
      return "red";
    default:
      return "gray";
  }
};

export default function AuditTable({ logs }: { logs: AuditLog[] }) {
  return (
    <Box bg="white" p={4} rounded="md" shadow="sm" overflowX="auto">
      <Table size="sm">
        <Thead>
          <Tr>
            <Th>Drawing</Th>
            <Th>User</Th>
            <Th>Action</Th>
            <Th>Status Change</Th>
            <Th>Date</Th>
          </Tr>
        </Thead>

        <Tbody>
          {logs.map((log) => (
            <Tr key={log.id}>
              <Td fontWeight="medium">{log.drawing_title}</Td>
              <Td>{log.user_name}</Td>
              <Td>
                <Badge colorScheme={actionColor(log.action)}>
                  {log.action}
                </Badge>
              </Td>
              <Td>
                {log.from_status
                  ? `${log.from_status} → ${log.to_status}`
                  : "—"}
              </Td>
              <Td>
                <Text fontSize="sm" color="gray.600">
                  {new Date(log.created_at).toLocaleString()}
                </Text>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}
