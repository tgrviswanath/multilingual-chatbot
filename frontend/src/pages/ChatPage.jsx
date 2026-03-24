import React, { useState, useRef, useEffect } from "react";
import {
  Box, TextField, IconButton, CircularProgress, Alert,
  Typography, Chip, FormControlLabel, Switch, Divider, Paper,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import { sendMessage } from "../services/chatApi";
import MessageBubble from "../components/MessageBubble";

const QUICK_MESSAGES = [
  { label: "👋 Hello", text: "Hello!" },
  { label: "💰 Pricing", text: "What are your pricing plans?" },
  { label: "🕐 Hours", text: "What are your business hours?" },
  { label: "🔄 Refund", text: "How do I get a refund?" },
  { label: "🇫🇷 French", text: "Bonjour, quels sont vos horaires?" },
  { label: "🇪🇸 Spanish", text: "¿Cuánto cuesta el servicio?" },
  { label: "🇩🇪 German", text: "Wie kann ich Sie kontaktieren?" },
];

const WELCOME = {
  role: "bot",
  text: "👋 Hello! I'm a multilingual FAQ chatbot. Ask me anything in English, French, Spanish, German, Italian, Portuguese, Dutch, Russian, Chinese, or Arabic!",
  meta: null,
};

export default function ChatPage() {
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [translateBack, setTranslateBack] = useState(true);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text = input) => {
    const msg = text.trim();
    if (!msg) return;
    setInput("");
    setError("");

    setMessages((prev) => [...prev, { role: "user", text: msg }]);
    setLoading(true);

    try {
      const res = await sendMessage(msg, translateBack);
      const data = res.data;
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.response,
          meta: {
            detected_language: data.detected_language,
            intent: data.intent,
            confidence: data.confidence,
            english_message: data.english_message,
          },
        },
      ]);
    } catch (e) {
      setError(e.response?.data?.detail || "Failed to get response.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "calc(100vh - 120px)" }}>

      {/* Controls row */}
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 1 }}>
        <FormControlLabel
          control={<Switch checked={translateBack} onChange={(e) => setTranslateBack(e.target.checked)} size="small" />}
          label={<Typography variant="body2">Translate response back to user language</Typography>}
        />
        <IconButton size="small" onClick={() => setMessages([WELCOME])} title="Reset chat">
          <RestartAltIcon fontSize="small" />
        </IconButton>
      </Box>

      {/* Quick message chips */}
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 1 }}>
        {QUICK_MESSAGES.map((q) => (
          <Chip key={q.label} label={q.label} size="small" variant="outlined"
            onClick={() => handleSend(q.text)} clickable
            disabled={loading}
          />
        ))}
      </Box>

      <Divider sx={{ mb: 1 }} />

      {/* Message list */}
      <Paper variant="outlined" sx={{ flex: 1, overflowY: "auto", p: 2, bgcolor: "grey.50" }}>
        {messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} />
        ))}
        {loading && (
          <Box sx={{ display: "flex", justifyContent: "flex-start", mb: 1 }}>
            <Box sx={{ px: 2, py: 1, bgcolor: "grey.100", borderRadius: "18px 18px 18px 4px" }}>
              <CircularProgress size={16} />
            </Box>
          </Box>
        )}
        <div ref={bottomRef} />
      </Paper>

      {error && <Alert severity="error" sx={{ mt: 1 }}>{error}</Alert>}

      {/* Input row */}
      <Box sx={{ display: "flex", gap: 1, mt: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={3}
          placeholder="Type a message in any language..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          size="small"
        />
        <IconButton
          color="primary"
          onClick={() => handleSend()}
          disabled={!input.trim() || loading}
          sx={{ bgcolor: "primary.main", color: "white", "&:hover": { bgcolor: "primary.dark" }, borderRadius: 2 }}
        >
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
}
