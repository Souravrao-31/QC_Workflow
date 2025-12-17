import { Flex, Heading, Spacer, Button, Badge } from "@chakra-ui/react";
import { decodeToken } from "../utils/jwt";
import { getToken, clearToken } from "../api/authStorage";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const token = getToken();
  const user = token ? decodeToken(token) : null;
  const navigate = useNavigate();

  const logout = () => {
    clearToken();
    window.location.href = "/";
  };
  const isAuditPage = location.pathname === "/audit";
  // console.log("User Info:", user);
  return (
    <Flex px={6} py={4} bg="blue.600" color="white" alignItems="center">
      <Heading size="md">QC Workflow System</Heading>

      <Spacer />

      {user?.role === "ADMIN" && (
        <>
          {isAuditPage ? (
            <Button
              size="sm"
              variant="ghost"
              mr={3}
              color="white"
              _hover={{ bg: "whiteAlpha.200" }}
              _active={{ bg: "whiteAlpha.300" }}
              onClick={() => navigate("/dashboard")}
            >
              Home
            </Button>
          ) : (
            <Button
              size="sm"
              variant="ghost"
              mr={3}
              color="white"
              _hover={{ bg: "whiteAlpha.200" }}
              _active={{ bg: "whiteAlpha.300" }}
              onClick={() => navigate("/audit")}
            >
              Audit Logs
            </Button>
          )}
        </>
      )}

      {user && (
        <Flex alignItems="center" gap={4}>
          <Badge colorScheme="purple">{user.role}</Badge>
          <Button size="sm" colorScheme="red" onClick={logout}>
            Logout
          </Button>
        </Flex>
      )}
    </Flex>
  );
}
