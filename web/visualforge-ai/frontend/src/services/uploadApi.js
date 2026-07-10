import apiClient from "./apiClient.js";

export const uploadApi = {
  upload(file, fileType = "asset") {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", fileType);
    return apiClient.post("/api/uploads", formData).then((res) => res.data);
  },
};
