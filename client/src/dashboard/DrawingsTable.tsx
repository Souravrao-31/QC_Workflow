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
  useToast,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { fetchDrawings, type Drawing } from "../api/drawings";
import { performDrawingAction } from "../api/drawings";
import { getAvailableActions } from "../utils/workflow";
import { useAuth } from "../auth/RequireAuth";

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
  const { user } = useAuth();
  const toast = useToast();
  const [drawings, setDrawings] = useState<Drawing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refreshDrawings = async () => {
    try {
      setLoading(true);
      const data = await fetchDrawings();
      setDrawings(data);
    } catch {
      setError("Failed to load drawings");
    } finally {
      setLoading(false);
    }
  };

  async function handleAction(
    drawingId: string,
    action: "CLAIM" | "SUBMIT" | "APPROVE"
  ) {
    try {
      await performDrawingAction(drawingId, action);
      toast({
        title: "Action successful",
        status: "success",
        duration: 2000,
      });
      refreshDrawings(); // re-fetch list
    } catch (err: any) {
      toast({
        title: "Action failed",
        description: err?.response?.data?.detail || "Something went wrong",
        status: "error",
        duration: 3000,
      });
    }
  }

  useEffect(() => {
    fetchDrawings()
      .then(setDrawings)
      .catch(() => setError("Failed to load drawings"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refreshDrawings();
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
  console.log("drawings.....", drawings);
  return (
    <Box bg="white" p={4} rounded="md" shadow="sm">
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Drawing Name</Th>
            <Th>Status</Th>
            <Th>Assigned To</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>

        <Tbody>
          {drawings.map((d) => (
            <Tr key={d?.title}>
              <Td>{d.title.slice(0, 15)}</Td>
              <Td>
                <Badge colorScheme={statusColor(d.status)}>{d.status}</Badge>
              </Td>
              <Td>{d.assigned_to_name ?? "—"}</Td>
              <Td>
                {getAvailableActions(
                  user.role,
                  d.status,
                  d.assigned_to === user.id
                ).map((action) => (
                  <Button
                    key={action}
                    size="sm"
                    mr={2}
                    colorScheme="blue"
                    onClick={() => handleAction(d.id, action)}
                  >
                    {action}
                  </Button>
                ))}
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}
