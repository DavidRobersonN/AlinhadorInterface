import { useCallback } from 'react'
import type { LedCommand, LedState } from '../types/led'
import type { MachineMessage } from '../types/machine'

type UseLedControlsParams = {
  send: (payload: { command: LedCommand }) => boolean
  lastMessage: MachineMessage | null
}

export function useLedControls({ send, lastMessage }: UseLedControlsParams) {
  const ledState: LedState =
    lastMessage?.type === 'led_status'
      ? lastMessage.state === 'ON'
        ? 'Ligado'
        : 'Desligado'
      : 'Desconhecido'

  const sendCommand = useCallback(
    (command: LedCommand) => {
      return send({ command })
    },
    [send],
  )

  const turnLedOn = useCallback(() => {
    sendCommand('ON')
  }, [sendCommand])

  const turnLedOff = useCallback(() => {
    sendCommand('OFF')
  }, [sendCommand])

  return {
    ledState,
    turnLedOn,
    turnLedOff,
  }
}