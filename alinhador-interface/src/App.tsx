import { useEffect, useRef, useState } from 'react'
import './App.css'

// Componente principal da aplicação
function App() {
  // Estado que guarda o texto do status do LED na tela
  // Começa como "Desconhecido" porque, ao abrir a página,
  // ainda não sabemos se o LED está ligado ou desligado
  const [ledState, setLedState] = useState<string>('Desconhecido')

  // Estado que guarda se a conexão WebSocket está ativa ou não
  // Começa como false porque, no início, ainda vamos tentar conectar
  const [connected, setConnected] = useState<boolean>(false)

  // useRef serve para guardar um valor que precisa continuar existindo
  // entre as renderizações do componente, sem causar nova renderização
  //
  // Aqui estamos guardando a instância do WebSocket.
  // Isso permite acessar a conexão depois, por exemplo,
  // quando clicarmos em um botão para enviar comandos.
  const socketRef = useRef<WebSocket | null>(null)

  // useEffect com array vazio [] executa apenas uma vez:
  // quando o componente aparece na tela
  //
  // É o lugar ideal para:
  // - abrir conexão WebSocket
  // - configurar eventos dessa conexão
  // - fazer limpeza ao sair da página
  useEffect(() => {
    // Cria a conexão WebSocket com o backend Django
    // Esse endereço precisa bater com a rota configurada no Django Channels
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/led/')

    // Guarda a conexão dentro da ref para podermos usar depois
    socketRef.current = socket

    // Evento disparado quando a conexão é aberta com sucesso
    socket.onopen = () => {
      console.log('WebSocket conectado')

      // Atualiza o estado para mostrar na interface que conectou
      setConnected(true)
    }

    // Evento disparado quando chega alguma mensagem do backend
    socket.onmessage = (event: MessageEvent) => {
      // event.data normalmente vem como texto JSON
      // então transformamos em objeto JavaScript
      const data = JSON.parse(event.data)

      // Verificamos o tipo da mensagem para saber como tratá-la
      // Aqui esperamos uma mensagem com type = 'led_status'
      if (data.type === 'led_status') {
        // Se o backend mandar "ON", mostramos "Ligado"
        // Caso contrário, mostramos "Desligado"
        setLedState(data.state === 'ON' ? 'Ligado' : 'Desligado')
      }
    }

    // Evento disparado quando a conexão fecha
    socket.onclose = () => {
      console.log('WebSocket desconectado')

      // Atualiza o estado para refletir desconexão na tela
      setConnected(false)
    }

    // Função de limpeza do useEffect
    // Executa quando o componente for desmontado
    // Exemplo: ao sair da página ou recarregar a aplicação
    return () => {
      // Fecha a conexão para evitar conexões abertas desnecessariamente
      socket.close()
    }
  }, [])

  // Função responsável por enviar um comando ao backend
  // Exemplo de comandos:
  // - ON
  // - OFF
  // - TOGGLE
  const sendCommand = (command: string) => {
    // Antes de enviar, verificamos:
    // 1. se existe uma conexão salva em socketRef.current
    // 2. se essa conexão está aberta
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) { // socketRef.current é a conexão WebSocket aberta com o Django.
      // Envia um JSON para o backend
      // O backend vai receber algo como:
      // { "command": "ON" }
      socketRef.current.send(JSON.stringify({ command }))
    }
  }

  // JSX = estrutura visual que será renderizada na tela
  return (
    <main className="app">
      <section className="card">
        {/* Título principal da interface */}
        <h1 className="title">LED com React + Django + Arduino</h1>

        <div className="statusBox">
          <p>
            {/* Mostra o estado da conexão com o backend */}
            <strong>Status da conexão:</strong>{' '}

            {/* A classe muda dependendo se está conectado ou não
                Isso permite mudar a cor no CSS */}
            <span className={connected ? 'connected' : 'disconnected'}>
              {connected ? 'Conectado' : 'Desconectado'}
            </span>
          </p>

          <p>
            {/* Mostra o estado atual do LED */}
            <strong>Estado do LED:</strong> {ledState}
          </p>
        </div>

        <div className="buttons">
          {/* Quando clicar, envia o comando ON para o backend */}
          <button onClick={() => sendCommand('ON')}>Ligar</button>

          {/* Quando clicar, envia o comando OFF para o backend */}
          <button onClick={() => sendCommand('OFF')}>Desligar</button>

          {/* Quando clicar, envia o comando TOGGLE para alternar o estado */}
          <button onClick={() => sendCommand('TOGGLE')}>Alternar</button>
        </div>
      </section>
    </main>
  )
}

// Exporta o componente para ser usado no restante do projeto
export default App