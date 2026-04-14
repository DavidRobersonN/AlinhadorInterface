import json
from channels.generic.websocket import WebsocketConsumer
from machine.services.machine_service import MachineService


class MachineConsumer(WebsocketConsumer):
    """
<<<<<<< HEAD
    Consumer responsável pela comunicação em tempo real
    entre o frontend React e o backend Django usando WebSocket.

    Pense nele como uma "porta de entrada" da máquina.

    Funções principais:
    - aceitar a conexão do frontend
    - receber mensagens em JSON
    - entregar essas mensagens para o MachineService
    - devolver a resposta para o frontend
    - encerrar conexões corretamente
=======
    Consumer responsável pela comunicação via WebSocket entre:

    - o frontend React
    - o backend Django
    - e os services da máquina

    Papel dele:
    1. aceitar a conexão do frontend
    2. receber mensagens em JSON
    3. enviar essas mensagens para o MachineService
    4. devolver a resposta para o frontend
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
    """

    def connect(self):
        """
<<<<<<< HEAD
        Este método é executado automaticamente
        quando o frontend abre a conexão WebSocket.

        O que fazemos aqui:
        1. criamos a instância do MachineService
        2. aceitamos a conexão
        3. enviamos uma mensagem inicial ao frontend
           informando que a conexão foi estabelecida
        """

        # Cria o service principal da máquina.
        # Ele será responsável por interpretar os comandos
        # e delegar a lógica para os serviços corretos.
        self.machine_service = MachineService()

        # Aceita oficialmente a conexão WebSocket.
        # Sem isso, o frontend tenta conectar, mas o backend não libera o acesso.
        self.accept()

        # Envia uma mensagem inicial para o frontend.
        # Isso é útil para a interface saber que a conexão foi aberta com sucesso.
=======
        Este método é executado automaticamente quando o frontend
        abre a conexão WebSocket com o backend.

        O que acontece aqui:
        - criamos uma instância do MachineService
        - aceitamos a conexão
        - enviamos uma mensagem inicial avisando que a conexão foi feita
        """

        # Cria o service principal da máquina.
        # Ele será responsável por interpretar os comandos recebidos
        # e delegar para o service correto.
        self.machine_service = MachineService()

        # Aceita a conexão WebSocket.
        # Sem isso, o frontend tenta conectar, mas a conexão não é aberta.
        self.accept()

        # Envia uma mensagem para o frontend informando
        # que a conexão com o backend foi estabelecida com sucesso.
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
        self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Conectado ao backend da máquina"
        }))

    def receive(self, text_data):
        """
<<<<<<< HEAD
        Este método é chamado automaticamente
        toda vez que o frontend envia uma mensagem pelo WebSocket.

        Exemplo de mensagem recebida:
        {
            "action": "led_on"
        }

        Fluxo interno:
        1. recebe o texto enviado pelo frontend
        2. converte esse texto JSON para dicionário Python
        3. envia os dados para o MachineService
        4. recebe a resposta pronta
        5. devolve essa resposta ao frontend
        """
=======
        CORAÇÃO DO CONSUMER: processamento das mensagens recebidas do frontend.
        Este método é executado automaticamente sempre que o frontend
        envia uma mensagem pelo WebSocket.

        O parâmetro text_data chega como texto.
        Exemplo:
        '{"action": "led_on"}'

        O fluxo aqui é:
        1. converter o texto JSON para dicionário Python
        2. passar os dados para o MachineService
        3. receber a resposta do service
        4. enviar essa resposta de volta para o frontend
        """

>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
        try:
            # Converte a string JSON recebida em um dicionário Python.
            # Exemplo:
            # '{"action": "led_on"}'
            # vira:
            # {"action": "led_on"}
            data = json.loads(text_data)

<<<<<<< HEAD
            # Entrega os dados recebidos para a camada de regra de negócio.
            # O MachineService decide o que fazer com esse comando.
            response = self.machine_service.handle_command(data)

            # Envia a resposta de volta para o frontend em formato JSON.
            # O frontend vai receber isso no WebSocket e atualizar a interface.
=======
            # Envia os dados recebidos para o service principal.
            # O MachineService decide qual regra executar
            # e qual service específico deve ser chamado.
            response = self.machine_service.handle_command(data)

            """
            Aqui, a variável response é a resposta do machine_service, que Vai para o Frontend.
            """
            # Envia a resposta do backend de volta para o frontend,
            # novamente em formato JSON.
            print("Resposta do backend para o frontend:", response)  # Log para depuração
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
            self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            """
            Este bloco trata erro de JSON inválido.

<<<<<<< HEAD
            Exemplo:
            se o frontend mandar algo mal formatado,
            como texto quebrado ou JSON incompleto,
            o json.loads() vai falhar.
=======
            Exemplo de erro:
            o frontend envia algo mal formatado, como:
            {action: led_on}
            em vez de:
            {"action": "led_on"}
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": "JSON inválido enviado pelo frontend"
            }))

        except Exception as error:
            """
<<<<<<< HEAD
            Este bloco captura qualquer outro erro inesperado.

            Exemplos:
            - erro dentro do MachineService
            - comando inexistente
            - falha ao acessar algum recurso
            - erro de conexão serial
=======
            Este bloco captura qualquer outro erro inesperado
            que aconteça durante o processamento da mensagem.

            Exemplo:
            - falha dentro do MachineService
            - erro ao acessar algum atributo
            - erro ao chamar algum service
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": str(error)
            }))

    def disconnect(self, close_code):
        """
<<<<<<< HEAD
        Este método é executado automaticamente
        quando a conexão WebSocket é encerrada.

        Isso pode acontecer quando:
        - o usuário fecha a página
        - o frontend derruba a conexão
        - o backend fecha a conexão
        - ocorre alguma falha

        Aqui tentamos liberar recursos corretamente,
        como conexões com serial, serviços ou estados internos.
        """
        try:
            # Verifica se o atributo machine_service existe antes de usar.
            # Isso evita erro caso a conexão tenha falhado antes da criação do service.
=======
        Este método é executado automaticamente quando a conexão WebSocket
        é encerrada.

        Exemplo:
        - usuário fecha a página
        - frontend perde conexão
        - socket é fechado manualmente

        Aqui tentamos encerrar corretamente recursos usados pelo service,
        como conexão serial com Arduino, se existir essa lógica no backend.
        """

        try:
            # Verifica se o atributo machine_service existe.
            # Isso evita erro caso a conexão seja encerrada
            # antes de o service ter sido criado.
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
            if hasattr(self, "machine_service"):
                # Chama o método de encerramento do service principal.
                # Esse método normalmente serve para fechar conexões,
                # limpar estados ou desconectar da porta serial.
                self.machine_service.disconnect()

        except Exception:
<<<<<<< HEAD
            # Se der erro ao desconectar, ignoramos silenciosamente
            # para não quebrar o encerramento do WebSocket.
=======
            # Se acontecer algum erro ao desconectar,
            # apenas ignoramos para não quebrar o encerramento do socket.
>>>>>>> 47ba729f215a104d88f7270af8d69636bac03193
            pass