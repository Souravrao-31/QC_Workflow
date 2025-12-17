import { Box, Text } from "@chakra-ui/react";

export default function EmptyState({ role }: { role: string }) {
  return (
    <Box bg="white" p={10} rounded="md" shadow="sm" textAlign="center">
      <Text fontSize="lg" fontWeight="semibold">
        No drawings available
      </Text>
      <Text color="gray.500" mt={2}>
        {role === "ADMIN" && "No unassigned drawings."}
        {role === "DRAFTER" && "No drawings available for drafting."}
        {role === "SHIFT_LEAD" && "No drawings waiting for First QC."}
        {role === "FINAL_QC" && "No drawings waiting for Final QC."}
      </Text>
    </Box>
  );
}
