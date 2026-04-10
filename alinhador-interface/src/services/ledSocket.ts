import type { LedCommand } from '../types/led'

// URL do WebSocket.
// Se amanhã você mudar o backend, altera aqui em um lugar só.
const LED_SOCKET_URL = 'ws://127.0.0.1:8000/ws/led/'

// Função responsável por criar a conexão WebSocket.
export function createLedSocket() {
  return new WebSocket(LED_SOCKET_URL)
}

// Função para enviar comando de forma padronizada para o backend.
export function sendLedCommand(socket: WebSocket, command: LedCommand) {
  socket.send(JSON.stringify({ command }))
}