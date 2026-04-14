import { useCallback, useEffect, useRef, useState } from 'react'
import { createMachineSocket, sendSocketMessage } from '../services/machineSocket'
import type { MachineMessage, MachinePayload } from '../types/machine'

// Hook principal da conexão da máquina.
// Ele cuida de:
// - abrir o WebSocket
// - fechar ao desmontar
// - guardar estado de conexão
// - guardar a última mensagem recebida
// - expor uma função genérica send
export function useMachineConnection() {
  const [connected, setConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<MachineMessage | null>(null)
  const [connectionError, setConnectionError] = useState<string | null>(null)

  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const socket = createMachineSocket()
    socketRef.current = socket

    socket.onopen = () => {
      console.log('WebSocket conectado')
      setConnected(true)
      setConnectionError(null)
    }

    socket.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data) as MachineMessage
        console.log('Mensagem parseada:', data)

        setLastMessage(data)

        if (data.type === 'error') {
          setConnectionError(data.message)
        }
      } catch (error) {
        console.error('Erro ao interpretar mensagem do WebSocket:', error)
      }
    }

    socket.onclose = () => {
      console.log('WebSocket desconectado')
      setConnected(false)
    }

    socket.onerror = () => {
      console.error('Erro no WebSocket')
      setConnectionError('Erro na conexão WebSocket')
    }

    return () => {
      socket.close()
      socketRef.current = null
    }
  }, [])

  const send = useCallback((payload: MachinePayload) => {
    const socket = socketRef.current

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket não está conectado')
      return false
    }

    sendSocketMessage(socket, payload)
    return true
  }, [])

  return {
    connected,
    lastMessage,
    connectionError,
    send,
  }
}