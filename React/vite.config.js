import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/react',
  plugins: [react()],
  optimizeDeps: {
    include: ['react-bootstrap', 'react-star-ratings']
  },
})
