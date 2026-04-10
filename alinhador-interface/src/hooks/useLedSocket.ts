import { useCallback, useEffect, useRef, useState } from 'react'
import { createLedSocket, sendLedCommand } from '../services/ledSocket'
import type { LedCommand, LedState, LedStatusMessage } from '../types/led'

// Hook customizado responsável por:
// - abrir a conexão WebSocket
// - ouvir mensagens do backend
// - guardar estado da conexão
// - guardar estado do LED
// - expor funções prontas para a interface
export function useLedSocket() {
  // Estado que mostra se a conexão com o backend está ativa
  const [connected, setConnected] = useState<boolean>(false)

  // Estado do LED mostrado na tela
  const [ledState, setLedState] = useState<LedState>('Desconhecido')

  // useRef guarda a instância do WebSocket sem causar nova renderização
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    // Cria a conexão WebSocket
    const socket = createLedSocket()

    // Guarda o socket na ref para poder usar depois
    socketRef.current = socket

    // Quando a conexão abrir com sucesso
    socket.onopen = () => {
      console.log('WebSocket conectado')
      setConnected(true)
    }

    // Quando chegar uma mensagem do backend
    socket.onmessage = (event: MessageEvent) => {
      try {
        // Converte o texto JSON em objeto JavaScript
        const data: LedStatusMessage = JSON.parse(event.data)

        // Verifica se a mensagem recebida é um status do LED
        if (data.type === 'led_status') {
          // Traduz o valor técnico do backend para algo amigável na tela
          setLedState(data.state === 'ON' ? 'Ligado' : 'Desligado')
        }
      } catch (error) {
        console.error('Erro ao interpretar mensagem do WebSocket:', error)
      }
    }

    // Quando a conexão fechar
    socket.onclose = () => {
      console.log('WebSocket desconectado')
      setConnected(false)
    }

    // Quando ocorrer erro na conexão
    socket.onerror = (error) => {
      console.error('Erro no WebSocket:', error)
    }

    // Limpeza ao desmontar o componente
    return () => {
      socket.close()
    }
  }, [])

  // Função genérica para enviar comandos ao backend.
  // useCallback evita recriar a função toda renderização.
  const sendCommand = useCallback((command: LedCommand) => {
    const socket = socketRef.current

    // Só envia se existir conexão e ela estiver aberta
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket não está conectado')
      return
    }

    sendLedCommand(socket, command)
  }, [])

  // Funções específicas para a interface usar com nomes mais claros
  const turnLedOn = useCallback(() => {
    sendCommand('ON')
  }, [sendCommand])

  const turnLedOff = useCallback(() => {
    sendCommand('OFF')
  }, [sendCommand])

  const toggleLed = useCallback(() => {
    sendCommand('TOGGLE')
  }, [sendCommand])

  return {
    connected,
    ledState,
    turnLedOn,
    turnLedOff,
    toggleLed,
  }
}