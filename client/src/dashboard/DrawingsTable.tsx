import {
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Spinner,
  Center,
  Text,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalCloseButton,
  useDisclosure,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import {
  fetchDrawings,
  fetchMyDrawings,
  performDrawingRelease,
  type Drawing,
} from "../api/drawings";
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

  const { isOpen, onOpen, onClose } = useDisclosure();
  const [releaseTarget, setReleaseTarget] = useState<string | null>(null);

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

  async function confirmRelease() {
    if (!releaseTarget) return;

    try {
      await performDrawingRelease(releaseTarget);

      toast({
        title: "Drawing released",
        description: "The drawing is now available for others",
        status: "success",
        duration: 2500,
      });

      loadData();
    } catch (err: any) {
      toast({
        title: "Release failed",
        description: err?.response?.data?.detail || "Something went wrong",
        status: "error",
        duration: 3000,
      });
    } finally {
      setReleaseTarget(null);
      onClose();
    }
  }

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
            <EmptyState role={user.role} personal={false} />
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
            <EmptyState role={user.role} personal={true} />
          ) : (
            <DrawingsTableView
              drawings={myWork}
              user={user}
              onAction={handleAction}
              //Available drawings are not owned yet, so releasing makes no sense.
              onRelease={(id: string) => {
                setReleaseTarget(id);
                onOpen(); // open confirmation modal
              }}
            />
          )}
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
