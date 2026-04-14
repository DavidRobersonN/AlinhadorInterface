// Tipo que representa os possíveis estados do LED na interface.
export type LedState = 'Ligado' | 'Desligado' | 'Desconhecido'

// Tipo para os comandos que o frontend envia ao backend.
<<<<<<< HEAD
export type LedCommand = 'ON' | 'OFF'
=======
export type LedCommand = 'ON' | 'OFF' 
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193

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