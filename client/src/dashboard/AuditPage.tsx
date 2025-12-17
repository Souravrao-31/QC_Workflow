import { useEffect, useState } from "react";
import { Center, Spinner, Text } from "@chakra-ui/react";
import { fetchAudit , type AuditLog } from "../api/drawings";
import AuditTable from "./AuditTable";

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

  return <AuditTable logs={logs} />;
}
