import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import 'bootstrap/dist/css/bootstrap.min.css'

import AppRoutes from './routes'; 

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error("Failed to find the root element. Check your index.html");
}

createRoot(rootElement).render(
  <StrictMode>
    <AppRoutes />
  </StrictMode>,
)
