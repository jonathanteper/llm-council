import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // Server configuration for Docker containerization
  // Implements: FR-2.3 (Frontend HMR Configuration)
  server: {
    // Bind to 0.0.0.0 to accept connections from outside the container
    host: '0.0.0.0',
    
    // Use standard Vite port
    port: 5173,
    
    // Enable strict port (fail if port is in use)
    strictPort: true,
    
    // HMR configuration for container networking
    hmr: {
      // Use the host's localhost for WebSocket connections
      // This allows HMR to work when accessing from host browser
      host: 'localhost',
    },
    
    // Watch configuration for volume mounts
    watch: {
      // Use polling as fallback if native file watching doesn't work
      // OrbStack typically doesn't need this, but Docker Desktop might
      usePolling: false,
    },
  },
})
