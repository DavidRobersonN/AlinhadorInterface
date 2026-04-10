
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Ponto de entrada da aplicação React.
// Aqui o React "entra" dentro da div com id="root" do index.html.
createRoot(document.getElementById('root')!).render(
  <App />
)