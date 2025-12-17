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
  HStack,
  VStack,
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
  if (!logs.length) {
    return (
      <Box bg="white" p={10} rounded="md" shadow="sm" textAlign="center">
        <Text fontSize="lg" fontWeight="semibold">
          No audit logs available
        </Text>
        <Text color="gray.500" mt={2}>
          Actions on drawings will appear here
        </Text>
      </Box>
    );
  }

  return (
    <Box
      bg="white"
      rounded="md"
      shadow="sm"
      overflowX="auto"
      border="1px solid"
      borderColor="gray.100"
    >
      <Table size="sm">
        <Thead position="sticky" top={0} bg="gray.50" zIndex={1}>
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
            <Tr
              key={log.id}
              _hover={{ bg: "gray.50" }}
              transition="background 0.2s"
            >
              {/* Drawing */}
              <Td>
                <Text fontWeight="semibold">{log.drawing_title}</Text>
              </Td>

              {/* User */}
              <Td>
                <VStack align="start" spacing={0}>
                  <Text fontSize="sm" fontWeight="medium">
                    {log.user_name || "—"}
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    {log.user_role}
                  </Text>
                </VStack>
              </Td>

              {/* Action */}
              <Td>
                <Badge
                  colorScheme={actionColor(log.action)}
                  px={2}
                  py={0.5}
                  rounded="md"
                >
                  {log.action}
                </Badge>
              </Td>

              {/* Status transition */}
              <Td>
                {log.from_status ? (
                  <HStack spacing={1}>
                    <Badge variant="subtle">{log.from_status}</Badge>
                    <Text fontSize="xs">→</Text>
                    <Badge variant="subtle" colorScheme="green">
                      {log.to_status}
                    </Badge>
                  </HStack>
                ) : (
                  "—"
                )}
              </Td>

              {/* Date */}
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
