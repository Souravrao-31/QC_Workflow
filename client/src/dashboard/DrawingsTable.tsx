import {
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Box,
  Spinner,
  Center,
  Text,
  useToast,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { fetchDrawings, fetchMyDrawings, type Drawing } from "../api/drawings";
import { performDrawingAction } from "../api/drawings";
import { useAuth } from "../auth/RequireAuth";
import DrawingsTableView from "./DrawingsTableView";
import EmptyState from "./EmptyState";

export default function DashboardPage() {
  const { user } = useAuth();
  const toast = useToast();

  const [available, setAvailable] = useState<Drawing[]>([]);
  const [myWork, setMyWork] = useState<Drawing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      setLoading(true);
      const [a, m] = await Promise.all([fetchDrawings(), fetchMyDrawings()]);
      setAvailable(a);
      setMyWork(m);
    } catch {
      setError("Failed to load drawings");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAction = async (id: string, action: any) => {
    try {
      await performDrawingAction(id, action);
      toast({ title: "Action successful", status: "success" });
      loadData();
    } catch (err: any) {
      toast({
        title: "Action failed",
        description: err?.response?.data?.detail,
        status: "error",
      });
    }
  };

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
    <Tabs variant="enclosed">
      {user.role !== "ADMIN" && (
        <TabList>
          <Tab>Available</Tab>
          <Tab>My Work</Tab>
        </TabList>
      )}

      <TabPanels>
        <TabPanel>
          {available.length === 0 ? (
            <EmptyState role={user.role} />
          ) : (
            <DrawingsTableView
              drawings={available}
              user={user}
              onAction={handleAction}
            />
          )}
        </TabPanel>

        <TabPanel>
          {myWork.length === 0 ? (
            <Box textAlign="center" py={10} color="gray.500">
              No drawings assigned to you
            </Box>
          ) : (
            <DrawingsTableView
              drawings={myWork}
              user={user}
              onAction={handleAction}
            />
          )}
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
