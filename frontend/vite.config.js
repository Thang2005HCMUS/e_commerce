import { defineConfig } from 'vite'
import React from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [React()],
  server: {
    port: 3000, // Bạn có thể đổi cổng chạy Front-end tại đây (mặc định của Vite thường là 5173)
  }
})