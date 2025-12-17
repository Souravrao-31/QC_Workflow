import { Box } from "@chakra-ui/react";
import Header from "./Header";
import Footer from "./Footer";
import DrawingsTable from "./DrawingsTable";


export default function DashboardPage() {
  return (
    <Box minH="100vh" display="flex" flexDirection="column">
      <Header />
      <Box flex="1" p={6} bg="gray.50">
        <DrawingsTable />
      </Box>
      <Footer />
    </Box>
  );
}
