import json
from channels.generic.websocket import WebsocketConsumer
from machine.services.machine_service import MachineService


class MachineConsumer(WebsocketConsumer):
    """
    Consumer responsável pela comunicação via WebSocket entre:

    - o frontend React
    - o backend Django
    - e os services da máquina

    Papel dele:
    1. aceitar a conexão do frontend
    2. receber mensagens em JSON
    3. enviar essas mensagens para o MachineService
    4. devolver a resposta para o frontend
    """

    def connect(self):
        """
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
        self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Conectado ao backend da máquina"
        }))

    def receive(self, text_data):
        """
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

        try:
            # Converte a string JSON recebida em um dicionário Python.
            # Exemplo:
            # '{"action": "led_on"}'
            # vira:
            # {"action": "led_on"}
            data = json.loads(text_data)

            # Envia os dados recebidos para o service principal.
            # O MachineService decide qual regra executar
            # e qual service específico deve ser chamado.
            response = self.machine_service.handle_command(data)

            # Envia a resposta do backend de volta para o frontend,
            # novamente em formato JSON.
            self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            """
            Este bloco trata erro de JSON inválido.

            Exemplo de erro:
            o frontend envia algo mal formatado, como:
            {action: led_on}
            em vez de:
            {"action": "led_on"}
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": "JSON inválido enviado pelo frontend"
            }))

        except Exception as error:
            """
            Este bloco captura qualquer outro erro inesperado
            que aconteça durante o processamento da mensagem.

            Exemplo:
            - falha dentro do MachineService
            - erro ao acessar algum atributo
            - erro ao chamar algum service
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": str(error)
            }))

    def disconnect(self, close_code):
        """
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
            if hasattr(self, "machine_service"):
                self.machine_service.disconnect()

        except Exception:
            # Se acontecer algum erro ao desconectar,
            # apenas ignoramos para não quebrar o encerramento do socket.
            pass