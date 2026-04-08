import { useEffect, useRef, useState } from 'react'

function App() {
  const [ledState, setLedState] = useState<string>('Desconhecido')
  const [connected, setConnected] = useState<boolean>(false)
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/led/')
    socketRef.current = socket

    socket.onopen = () => {
      console.log('WebSocket conectado')
      setConnected(true)
    }

    socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data)

      if (data.type === 'led_status') {
        setLedState(data.state === 'ON' ? 'Ligado' : 'Desligado')
      }
    }

    socket.onclose = () => {
      console.log('WebSocket desconectado')
      setConnected(false)
    }

    return () => {
      socket.close()
    }
  }, [])

  const sendCommand = (command: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ command }))
    }
  }

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial' }}>
      <h1>Controle de LED com React + Django + Arduino</h1>

      <p>
        <strong>Status da conexão:</strong>{' '}
        {connected ? 'Conectado' : 'Desconectado'}
      </p>

      <p>
        <strong>Estado do LED:</strong> {ledState}
      </p>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={() => sendCommand('ON')}>Ligar</button>
        <button onClick={() => sendCommand('OFF')}>Desligar</button>
        <button onClick={() => sendCommand('TOGGLE')}>Alternar</button>
      </div>
    </div>
  )
}

export default App