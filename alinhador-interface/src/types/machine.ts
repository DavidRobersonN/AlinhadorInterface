import type { LedStatusMessage, LedCommand } from './led'

export interface ConnectionMessage {
  type: 'connection'
  status: 'connected' | 'disconnected'
  message: string
}

export interface ErrorMessage {
  type: 'error'
  message: string
}

export type MachineMessage =
  | LedStatusMessage
  | ConnectionMessage
  | ErrorMessage

export type MachinePayload = {
  command: LedCommand
}