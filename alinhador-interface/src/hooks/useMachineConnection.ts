import { useCallback, useEffect, useRef, useState } from 'react'
import { createMachineSocket, sendSocketMessage } from '../services/machineSocket'
import type { LedStatusMessage, LedCommand } from '../types/led'

// Tipo do payload que o frontend envia pelo WebSocket.
// Neste momento, a aplicação envia apenas comandos relacionados ao LED.
type LedPayload = {
  command: LedCommand
}

// Hook principal responsável por:
// - abrir a conexão WebSocket
// - acompanhar o status da conexão
// - guardar a última mensagem recebida do backend
// - disponibilizar uma função genérica de envio de comandos
export function useMachineConnection() {
<<<<<<< HEAD
  const [connected, setConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<MachineMessage | null>(null)
=======
  // Estado que informa se o WebSocket está conectado.
  const [connected, setConnected] = useState<boolean>(false)

  // Guarda a última mensagem recebida do backend.
  // Como o projeto está focado apenas no LED, a mensagem esperada é LedStatusMessage.
  const [lastMessage, setLastMessage] = useState<LedStatusMessage | null>(null)

  // Guarda uma possível mensagem de erro da conexão.
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
  const [connectionError, setConnectionError] = useState<string | null>(null)

  // useRef armazena a instância do WebSocket sem causar re-renderizações.
  // Isso permite reutilizar a conexão nas funções do hook.
  const socketRef = useRef<WebSocket | null>(null)

  // Effect executado uma única vez ao montar o componente.
  // Ele cria a conexão WebSocket e registra os eventos principais.
  useEffect(() => {
    // Cria a conexão com o backend.
    const socket = createMachineSocket()

    // Guarda a instância do socket na ref para uso posterior.
    socketRef.current = socket

    // Evento disparado quando a conexão é aberta com sucesso.
    socket.onopen = () => {
      console.log('WebSocket conectado')
      setConnected(true)
      setConnectionError(null)
    }

    // Evento disparado sempre que uma nova mensagem chega do backend.
    socket.onmessage = (event: MessageEvent) => {
      try {
<<<<<<< HEAD
        const data = JSON.parse(event.data) as MachineMessage
        console.log('Mensagem parseada:', data)

=======
        // Converte a mensagem JSON recebida em objeto JavaScript.
        const data: LedStatusMessage = JSON.parse(event.data)

        // Log útil para depuração durante o desenvolvimento.
        console.log('Mensagem recebida no socket:', data)

        // Atualiza o estado com a última mensagem recebida.
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
        setLastMessage(data)

        if (data.type === 'error') {
          setConnectionError(data.message)
        }
      } catch (error) {
        // Se a mensagem vier em formato inválido, registra o erro no console.
        console.error('Erro ao interpretar mensagem do WebSocket:', error)
      }
    }

    // Evento disparado quando a conexão é encerrada.
    socket.onclose = () => {
      console.log('WebSocket desconectado')
      setConnected(false)
    }

    // Evento disparado em caso de erro no WebSocket.
    socket.onerror = () => {
      console.error('Erro no WebSocket')
      setConnectionError('Erro na conexão WebSocket')
    }

    // Função de limpeza executada ao desmontar o componente.
    // Fecha a conexão para evitar conexões abertas desnecessariamente.
    return () => {
      socket.close()
      socketRef.current = null
    }
  }, [])

  // Função genérica para enviar mensagens ao backend.
  // useCallback evita recriar a função em toda renderização.
  const send = useCallback((payload: LedPayload) => {
    const socket = socketRef.current

    // Impede envio caso o socket não exista ou ainda não esteja conectado.
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket não está conectado')
      return false
    }

    // Envia a mensagem para o backend.
    sendSocketMessage(socket, payload)
    return true
  }, [])

  // O hook retorna os estados e a função de envio
  // para serem usados por outros hooks ou componentes da interface.
  return {
    connected,
    lastMessage,
    connectionError,
    send,
  }
}