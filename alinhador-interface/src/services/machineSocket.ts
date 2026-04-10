// Serviço responsável apenas pela parte técnica do WebSocket.
// Aqui não colocamos regra de LED, motor ou interface.
// Ele só cria a conexão e envia mensagens.

export function createMachineSocket(): WebSocket {
  return new WebSocket('ws://127.0.0.1:8000/ws/led/')
}

export function sendSocketMessage(
  socket: WebSocket,
  payload: Record<string, unknown>,
): void {
  socket.send(JSON.stringify(payload))
}