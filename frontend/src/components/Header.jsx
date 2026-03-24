import { AppBar, Toolbar, Typography } from "@mui/material";
import ChatIcon from "@mui/icons-material/Chat";

export default function Header() {
  return (
    <AppBar position="static" color="primary">
      <Toolbar sx={{ gap: 1 }}>
        <ChatIcon />
        <Typography variant="h6" fontWeight="bold">
          Multilingual FAQ Chatbot
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
