import apiClient from "./apiClient.js";

function buildFormData(payload) {
  const formData = new FormData();
  Object.entries(payload).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      formData.append(key, value);
    }
  });
  return formData;
}

export const generationApi = {
  textToImage(payload) {
    return apiClient
      .post("/api/text-to-image", buildFormData(payload))
      .then((res) => res.data);
  },
  imageToImage(payload) {
    return apiClient
      .post("/api/image-to-image", buildFormData(payload))
      .then((res) => res.data);
  },
  inpaint(payload) {
    return apiClient
      .post("/api/inpaint", buildFormData(payload))
      .then((res) => res.data);
  },
  list(params = {}) {
    return apiClient.get("/api/generations", { params }).then((res) => res.data);
  },
  get(id) {
    return apiClient.get(`/api/generations/${id}`).then((res) => res.data);
  },
  remove(id) {
    return apiClient.delete(`/api/generations/${id}`).then((res) => res.data);
  },
};
