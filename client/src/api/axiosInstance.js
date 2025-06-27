import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5555", // or your actual API URL
});

// Auto-attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
