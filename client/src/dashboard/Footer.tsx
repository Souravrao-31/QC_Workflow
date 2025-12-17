import { Box, Text } from "@chakra-ui/react";

export default function Footer() {
  return (
    <Box py={3} textAlign="center" bg="gray.100">
      <Text fontSize="sm" color="gray.600">
        QC Workflow System • v1.0 • All actions are audited
      </Text>
    </Box>
  );
}
