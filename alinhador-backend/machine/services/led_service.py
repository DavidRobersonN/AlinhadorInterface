class LedService:
    """
    Service responsável apenas pelas ações relacionadas ao LED.
    """

    def __init__(self, serial_service):
        self.serial_service = serial_service

    def led_on(self) -> dict:
        serial_result = self.serial_service.send_command("LED_ON")

        return {
            "type": "led_status",
            "state": "ON",
            "message": "Comando para ligar LED enviado com sucesso",
            "serial": serial_result,
        }

    def led_off(self) -> dict:
        serial_result = self.serial_service.send_command("LED_OFF")

        return {
            "type": "led_status",
            "state": "OFF",
            "message": "Comando para desligar LED enviado com sucesso",
            "serial": serial_result,
        }

