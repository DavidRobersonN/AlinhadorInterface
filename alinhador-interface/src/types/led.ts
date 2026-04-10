// Tipo que representa os possíveis estados do LED na interface.
export type LedState = 'Ligado' | 'Desligado' | 'Desconhecido'

// Tipo para os comandos que o frontend envia ao backend.
export type LedCommand = 'ON' | 'OFF' | 'TOGGLE'

// Tipo esperado para as mensagens recebidas do backend.
// Exemplo:
// {
//   "type": "led_status",
//   "state": "ON"
// }
export interface LedStatusMessage {
  type: 'led_status'
  state: 'ON' | 'OFF'
}