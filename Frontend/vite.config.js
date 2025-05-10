import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/cnninfer': 'http://localhost:8000',
      '/mlpinfer': 'http://localhost:8000',
      '/lorinfer': 'http://localhost:8000',
      '/feedback': 'http://localhost:8000',
    }
  }
})
