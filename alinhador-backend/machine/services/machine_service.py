from machine.services.serial_service import SerialService
from machine.services.led_service import LedService
from machine.services.motor_service import MotorService


class MachineService:
    """
    Orquestrador principal da máquina.

    Recebe os comandos e delega para o service correto.
    """

    def __init__(self):
        self.serial_service = SerialService()
        self.led_service = LedService(self.serial_service)
        self.motor_service = MotorService(self.serial_service)

    def handle_command(self, data: dict) -> dict:
        action = data.get("action")
        legacy_command = data.get("command")

        # Compatibilidade com frontend antigo
        if legacy_command == "ON":
            return self.led_service.led_on()

        if legacy_command == "OFF":
            return self.led_service.led_off()

        if legacy_command == "TOGGLE":
            return self.led_service.toggle_led()

        # Novo padrão
        if action == "ping":
            return self._handle_ping()

        if action == "led_on":
            return self.led_service.led_on()

        if action == "led_off":
            return self.led_service.led_off()

        if action == "toggle_led":
            return self.led_service.toggle_led()

        if action == "rotate_motor":
            return self.motor_service.rotate_motor(data)

        return {
            "type": "error",
            "message": f"Ação inválida: {action or legacy_command}"
        }

    def _handle_ping(self) -> dict:
        return {
            "type": "pong",
            "message": "Backend respondeu com sucesso"
        }

    def disconnect(self) -> None:
        """
        Fecha a conexão serial quando o websocket for encerrado.
        """
        self.serial_service.disconnect()