import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backendProxy = {
  "/admin": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
  "/api": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
  "/media": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
  "/static": {
    target: "http://127.0.0.1:8000/",
    changeOrigin: true,
  },
};

const publicPreviewProxy = {
  "/api": backendProxy["/api"],
  "/media": backendProxy["/media"],
};

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: backendProxy,
  },
  preview: {
    allowedHosts: [".trycloudflare.com"],
    proxy: publicPreviewProxy,
  },
});
