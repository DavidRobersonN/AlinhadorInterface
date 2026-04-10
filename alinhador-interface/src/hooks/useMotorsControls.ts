import { useCallback, useEffect, useState } from 'react'
import type { LedCommand, LedState, LedStatusMessage } from '../types/led'
import type { MachineMessage } from '../types/machine'

type UseLedControlsParams = {
  send: (payload: Record<string, unknown>) => boolean
  lastMessage: MachineMessage | null
}

// Hook responsável apenas pela parte do LED.
// Ele:
// - lê mensagens do tipo led_status
// - atualiza o estado do LED
// - expõe funções prontas para a interface
export function useLedControls({ send, lastMessage }: UseLedControlsParams) {
  const [ledState, setLedState] = useState<LedState>('Desconhecido')

  useEffect(() => {
    if (!lastMessage) return

    if (lastMessage.type === 'led_status') {
      const data = lastMessage as LedStatusMessage
      setLedState(data.state === 'ON' ? 'Ligado' : 'Desligado')
    }
  }, [lastMessage])

  const sendCommand = useCallback(
    (command: LedCommand) => {
      send({ command })
    },
    [send],
  )

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
    ledState,
    turnLedOn,
    turnLedOff,
    toggleLed,
  }
}