class MotorService:
    """
    Service responsável apenas pelas ações relacionadas ao motor.
    """

    STEPS_PER_TURN = 400

    def __init__(self, serial_service):
        self.serial_service = serial_service

    def rotate_motor(self, data: dict) -> dict:
        direction = data.get("direction")
        turns = data.get("turns")
        steps = data.get("steps")

        sent = self._translate_direction(direction)

        if turns is not None:
            steps = self._turns_to_steps(turns)

        if steps is None:
            return {
                "type": "error",
                "message": "É necessário informar 'turns' ou 'steps'"
            }

        if int(steps) <= 0:
            return {
                "type": "error",
                "message": "A quantidade de passos deve ser maior que zero"
            }

        command = f"MOTOR:{sent}:{int(steps)}"
        serial_result = self.serial_service.send_command(command)

        return {
            "type": "motor_status",
            "message": "Comando de motor enviado com sucesso",
            "direction": direction,
            "steps": int(steps),
            "command": command,
            "serial": serial_result,
        }

    def _translate_direction(self, direction: str) -> int:
        if direction == "tighten":
            return 1

        if direction == "loosen":
            return -1

        raise Exception("Direção inválida. Use 'tighten' ou 'loosen'.")

    def _turns_to_steps(self, turns) -> int:
        return int(float(turns) * self.STEPS_PER_TURN)