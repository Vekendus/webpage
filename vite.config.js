import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backendProxy = {
  "/api": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
  "/media": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
};

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: backendProxy,
  },
  preview: {
    allowedHosts: ["youth-fort-leu-sue.trycloudflare.com"],
    proxy: backendProxy,
  },
});
