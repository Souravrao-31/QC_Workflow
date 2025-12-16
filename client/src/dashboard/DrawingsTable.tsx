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

const mockDrawings = [
  {
    id: "D-101",
    status: "DRAFTING",
    assigned_to: "Drafter One",
  },
  {
    id: "D-102",
    status: "FIRST_QC",
    assigned_to: null,
  },
];

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
          {mockDrawings.map((d) => (
            <Tr key={d.id}>
              <Td>{d.id}</Td>
              <Td>
                <Badge colorScheme={statusColor(d.status)}>
                  {d.status}
                </Badge>
              </Td>
              <Td>{d.assigned_to ?? "—"}</Td>
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
