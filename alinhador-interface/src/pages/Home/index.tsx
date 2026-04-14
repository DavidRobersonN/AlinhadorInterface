import { LedControlCard } from '../../components/led/LedControlCard'
import { useMachineConnection } from '../../hooks/useMachineConnection'
import { useLedControls } from '../../hooks/useLedControls'

// Página principal da aplicação.
// Ela conecta a lógica dos hooks com o componente visual.
export function HomePage() {
  // Hook principal da conexão com a máquina
  const { connected, lastMessage, send } = useMachineConnection()

  // Hook específico do LED, usando a conexão principal
  const { ledState, turnLedOn, turnLedOff } = useLedControls({
    send,
    lastMessage,
  })

  return (
    <main className="app">
      <LedControlCard
        connected={connected}
        ledState={ledState}
        onTurnOn={turnLedOn}
        onTurnOff={turnLedOff}
      />
    </main>
  )
}