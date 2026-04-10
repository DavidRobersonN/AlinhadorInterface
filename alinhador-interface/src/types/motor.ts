export type MotorDirection = 'tighten' | 'loosen'

export interface RotateMotorPayload {
  action: 'rotate_motor'
  direction: MotorDirection
  turns?: number
  steps?: number
}

export interface MotorStatusMessage {
  type: 'motor_status'
  message: string
  direction: MotorDirection
  steps: number
  command: string
  serial?: {
    success: boolean
    command_sent: string
  }
}