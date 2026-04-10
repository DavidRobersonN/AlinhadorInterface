interface ConnectionStatusProps {
  connected: boolean
}

// Componente visual responsável apenas por mostrar o status da conexão.
// Ele não sabe nada sobre WebSocket.
// Apenas recebe uma prop e renderiza.
export function ConnectionStatus({ connected }: ConnectionStatusProps) {
  return (
    <p>
      <strong>Status da conexão:</strong>{' '}
      <span className={connected ? 'connected' : 'disconnected'}>
        {connected ? 'Conectado' : 'Desconectado'}
      </span>
    </p>
  )
}