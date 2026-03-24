import axios from "axios";

const api = axios.create({ baseURL: process.env.REACT_APP_API_URL });

export const sendMessage = (message, translateResponse = true) =>
  api.post("/api/v1/chat", { message, translate_response: translateResponse });
