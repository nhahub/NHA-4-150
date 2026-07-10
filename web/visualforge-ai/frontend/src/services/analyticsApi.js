import apiClient from "./apiClient.js";

export const analyticsApi = {
  summary() {
    return apiClient.get("/api/analytics/summary").then((res) => res.data);
  },
  charts() {
    return apiClient.get("/api/analytics/charts").then((res) => res.data);
  },
};
