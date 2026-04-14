import json
from channels.generic.websocket import WebsocketConsumer
from machine.services.machine_service import MachineService


class MachineConsumer(WebsocketConsumer):
    """
    Consumer responsável pela comunicação em tempo real
    entre o frontend React e o backend Django usando WebSocket.

    Pense nele como uma "porta de entrada" da máquina.

    Funções principais:
    - aceitar a conexão do frontend
    - receber mensagens em JSON
    - entregar essas mensagens para o MachineService
    - devolver a resposta para o frontend
    - encerrar conexões corretamente
    """

    def connect(self):
        """
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
        self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Conectado ao backend da máquina"
        }))

    def receive(self, text_data):
        """
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
        try:
            # Converte a string JSON recebida em um dicionário Python.
            # Exemplo:
            # '{"action": "led_on"}'
            # vira:
            # {"action": "led_on"}
            data = json.loads(text_data)

            # Entrega os dados recebidos para a camada de regra de negócio.
            # O MachineService decide o que fazer com esse comando.
            response = self.machine_service.handle_command(data)

            # Envia a resposta de volta para o frontend em formato JSON.
            # O frontend vai receber isso no WebSocket e atualizar a interface.
            self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            """
            Este bloco trata erro de JSON inválido.

            Exemplo:
            se o frontend mandar algo mal formatado,
            como texto quebrado ou JSON incompleto,
            o json.loads() vai falhar.
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": "JSON inválido enviado pelo frontend"
            }))

        except Exception as error:
            """
            Este bloco captura qualquer outro erro inesperado.

            Exemplos:
            - erro dentro do MachineService
            - comando inexistente
            - falha ao acessar algum recurso
            - erro de conexão serial
            """

            self.send(text_data=json.dumps({
                "type": "error",
                "message": str(error)
            }))

    def disconnect(self, close_code):
        """
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
            if hasattr(self, "machine_service"):
                # Chama o método de encerramento do service principal.
                # Esse método normalmente serve para fechar conexões,
                # limpar estados ou desconectar da porta serial.
                self.machine_service.disconnect()

        except Exception:
            # Se der erro ao desconectar, ignoramos silenciosamente
            # para não quebrar o encerramento do WebSocket.
            pass