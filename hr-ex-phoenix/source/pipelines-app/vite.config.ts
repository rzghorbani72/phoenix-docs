import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

// One self-contained index.html (JS, CSS and data inlined) so it opens from disk without a server.
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  base: "./",
  build: { outDir: "../../technical/phoenix-pipelines/app", emptyOutDir: true, chunkSizeWarningLimit: 4000 },
});
