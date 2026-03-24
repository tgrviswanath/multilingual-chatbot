import { Box, Typography, Chip, Tooltip } from "@mui/material";

const LANG_FLAGS = {
  en: "🇬🇧", fr: "🇫🇷", es: "🇪🇸", de: "🇩🇪",
  it: "🇮🇹", pt: "🇵🇹", nl: "🇳🇱", ru: "🇷🇺",
  "zh-cn": "🇨🇳", ar: "🇸🇦",
};

export default function MessageBubble({ msg }) {
  const isUser = msg.role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 1.5,
      }}
    >
      <Box sx={{ maxWidth: "75%" }}>
        <Box
          sx={{
            px: 2, py: 1.5,
            borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
            bgcolor: isUser ? "primary.main" : "grey.100",
            color: isUser ? "white" : "text.primary",
          }}
        >
          <Typography variant="body1">{msg.text}</Typography>
        </Box>

        {/* Metadata row for bot messages */}
        {!isUser && msg.meta && (
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mt: 0.5, pl: 1 }}>
            {msg.meta.detected_language && (
              <Tooltip title={`Detected: ${msg.meta.detected_language}`}>
                <Chip
                  label={`${LANG_FLAGS[msg.meta.detected_language] || "🌐"} ${msg.meta.detected_language}`}
                  size="small" variant="outlined" sx={{ fontSize: "0.7rem" }}
                />
              </Tooltip>
            )}
            {msg.meta.intent && (
              <Chip label={`intent: ${msg.meta.intent}`} size="small"
                color="primary" variant="outlined" sx={{ fontSize: "0.7rem" }} />
            )}
            {msg.meta.confidence !== undefined && (
              <Chip label={`${(msg.meta.confidence * 100).toFixed(0)}%`} size="small"
                variant="outlined" sx={{ fontSize: "0.7rem" }} />
            )}
            {msg.meta.english_message && msg.meta.detected_language !== "en" && (
              <Tooltip title={`Translated: "${msg.meta.english_message}"`}>
                <Chip label="translated" size="small" color="info"
                  variant="outlined" sx={{ fontSize: "0.7rem", cursor: "help" }} />
              </Tooltip>
            )}
          </Box>
        )}
      </Box>
    </Box>
  );
}
