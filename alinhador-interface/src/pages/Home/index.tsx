import { LedControlCard } from '../../components/led/LedControlCard'
import { useMachineConnection } from '../../hooks/useMachineConnection'
import { useLedControls } from '../../hooks/useLedControls'

// Página principal da aplicação.
// Ela conecta a lógica dos hooks com o componente visual.
export function HomePage() {
  // Hook principal responsável pela conexão WebSocket com o backend.
  // Ele fornece:
  // - o estado da conexão
  // - a última mensagem recebida
  // - a função genérica de envio de comandos
  const { connected, lastMessage, send } = useMachineConnection()

  // Hook responsável apenas pelas regras do LED.
  // Ele recebe a função de envio e a última mensagem da conexão principal,
  // e devolve:
  // - o estado atual do LED para a interface
  // - as ações prontas para ligar, desligar e alternar
  const { ledState, turnLedOn, turnLedOff } = useLedControls({
    send,
    lastMessage,
  })
    console.log('LedControlCard renderizou. ledState =', ledState)


  // A página apenas repassa os dados e ações para o componente visual.
  // Assim, a lógica fica nos hooks e a interface fica mais limpa.
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