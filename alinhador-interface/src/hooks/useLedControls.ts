<<<<<<< HEAD
import { useCallback } from 'react'
import type { LedCommand, LedState } from '../types/led'
import type { MachineMessage } from '../types/machine'

type UseLedControlsParams = {
  send: (payload: { command: LedCommand }) => boolean
  lastMessage: MachineMessage | null
=======
import { useCallback, useEffect, useState } from 'react'
import type { LedCommand, LedState, LedStatusMessage } from '../types/led'

type LedPayload = {
  command: LedCommand
}

type UseLedControlsParams = {
  send: (payload: LedPayload) => boolean
  lastMessage: LedStatusMessage | null
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
}

export function useLedControls({ send, lastMessage }: UseLedControlsParams) {
<<<<<<< HEAD
  const ledState: LedState =
    lastMessage?.type === 'led_status'
      ? lastMessage.state === 'ON'
        ? 'Ligado'
        : 'Desligado'
      : 'Desconhecido'
=======
  const [ledState, setLedState] = useState<LedState>('Desconhecido')

  useEffect(() => {
    if (!lastMessage) return

    if (lastMessage.type === 'led_status') {
      setLedState(lastMessage.state === 'ON' ? 'Ligado' : 'Desligado')
    }
  }, [lastMessage])
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193

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