import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Standard Vite React app. Files in public/ (docs, drawio) are copied to dist/ unchanged;
// base "./" keeps the build working from any sub-path or static file server.
export default defineConfig({
  plugins: [react()],
  base: "./",
});
