import apiClient from "../../../services/apiClient.js";

export const chatbotApi = {
  sendMessage(message, sessionId = "default") {
    return apiClient
      .post("/api/chatbot/message", {
        message,
        session_id: sessionId,
      })
      .then((res) => res.data);
  },
  history(sessionId = "default") {
    return apiClient
      .get("/api/chatbot/history", { params: { session_id: sessionId } })
      .then((res) => res.data);
  },
  clear(sessionId = "default") {
    return apiClient
      .delete("/api/chatbot/history", { params: { session_id: sessionId } })
      .then((res) => res.data);
  },
};
