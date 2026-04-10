import json
from channels.generic.websocket import WebsocketConsumer
from machine.services.machine_service import MachineService


class MachineConsumer(WebsocketConsumer):
    """
    Consumer responsável por:

    - aceitar conexão WebSocket do React
    - receber mensagens em JSON
    - chamar o service que contém a regra de negócio
    - enviar resposta de volta ao frontend
    """

    def connect(self):
        self.machine_service = MachineService()
        self.accept()

        self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "Conectado ao backend da máquina"
        }))

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            response = self.machine_service.handle_command(data)
            self.send(text_data=json.dumps(response))

        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                "type": "error",
                "message": "JSON inválido enviado pelo frontend"
            }))

        except Exception as error:
            self.send(text_data=json.dumps({
                "type": "error",
                "message": str(error)
            }))

    def disconnect(self, close_code):
        try:
            if hasattr(self, "machine_service"):
                self.machine_service.disconnect()
        except Exception:
            pass