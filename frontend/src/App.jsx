import React from "react";
import { Container } from "@mui/material";
import Header from "./components/Header";
import ChatPage from "./pages/ChatPage";

export default function App() {
  return (
    <>
      <Header />
      <Container maxWidth="md" sx={{ py: 2 }}>
        <ChatPage />
      </Container>
    </>
  );
}
