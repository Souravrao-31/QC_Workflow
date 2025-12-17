import { useEffect, useState } from "react";
import { Center, Spinner, Text, Box } from "@chakra-ui/react";
import { fetchAudit, type AuditLog } from "../api/drawings";
import AuditTable from "./AuditTable";
import Header from "./Header";
import Footer from "./Footer";
export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAudit()
      .then(setLogs)
      .catch(() => setError("Failed to load audit logs"))
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

  if (logs.length === 0) {
    return (
      <Center py={20}>
        <Text color="gray.500">No audit logs available</Text>
      </Center>
    );
  }

  return (
    <Box minH="100vh" display="flex" flexDirection="column">
      <Header />
      <Box flex="1" p={6} bg="gray.50">
        <AuditTable logs={logs} />
      </Box>
      <Footer />
    </Box>
  );
}
