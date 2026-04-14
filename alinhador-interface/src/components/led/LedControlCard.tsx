
import type { LedState } from '../../types/led'
import { ActionButton } from '../common/ActionButton'
import { ConnectionStatus } from '../common/ConnectionStatus'

interface LedControlCardProps {
  connected: boolean
  ledState: LedState
  onTurnOn: () => void
  onTurnOff: () => void
}

// Componente visual principal do módulo do LED.
// Ele recebe os dados e as funções prontas via props.
export function LedControlCard({
  connected,
  ledState,
  onTurnOn,
  onTurnOff,
}: LedControlCardProps) {
  return (
    <section className="card">
      <h1 className="title">LED com React + Django + Arduino</h1>

      <div className="statusBox">
        <ConnectionStatus connected={connected} />

        <p>
          <strong>Estado do LED:</strong> {ledState}
        </p>
      </div>

      <div className="buttons">
        <ActionButton onClick={onTurnOn} disabled={!connected}>
          Ligar
        </ActionButton>

        <ActionButton onClick={onTurnOff} disabled={!connected}>
          Desligar
        </ActionButton>
      </div>
    </section>
  )
}