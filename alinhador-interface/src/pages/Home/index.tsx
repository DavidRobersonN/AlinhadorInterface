import { LedControlCard } from '../../components/led/LedControlCard'
import { useLedSocket } from '../../hooks/useLedSocket'

// Página principal da aplicação.
// Ela conecta a lógica do hook com os componentes visuais.
export function HomePage() {
  const { connected, ledState, turnLedOn, turnLedOff, toggleLed } = useLedSocket()

  return (
    <main className="app">
      <LedControlCard
        connected={connected}
        ledState={ledState}
        onTurnOn={turnLedOn}
        onTurnOff={turnLedOff}
        onToggle={toggleLed}
      />
    </main>
  )
}