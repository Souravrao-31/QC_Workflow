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
  Spinner,
  Center,
  Text,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { fetchDrawings, type Drawing } from "../api/drawings";

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

export default function DrawingsTable() {
  const [drawings, setDrawings] = useState<Drawing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDrawings()
      .then(setDrawings)
      .catch(() => setError("Failed to load drawings"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <Center py={20}>
        <Spinner size="xl" />
      </Center>
    );
  }

  if (error) {
    return (
      <Center py={20}>
        <Text color="red.500">{error}</Text>
      </Center>
    );
  }

  return (
    <Box bg="white" p={4} rounded="md" shadow="sm">
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Drawing ID</Th>
            <Th>Status</Th>
            <Th>Assigned To</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>

        <Tbody>
          {drawings.map((d) => (
            <Tr key={d.id}>
              <Td>{d.id.slice(0, 8)}</Td>
              <Td>
                <Badge colorScheme={statusColor(d.status)}>
                  {d.status}
                </Badge>
              </Td>
              <Td>{d.assigned_to_name ?? "—"}</Td>
              <Td>
                <Button size="sm" colorScheme="blue">
                  Claim
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}
