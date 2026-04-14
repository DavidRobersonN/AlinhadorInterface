from machine.services.serial_service import SerialService
from machine.services.led_service import LedService


class MachineService:
    """
    Service principal da máquina.

    Ele funciona como um ORQUESTRADOR.

    Isso significa que ele:
    - recebe os dados vindos do consumer
    - identifica qual comando foi enviado
    - decide para qual service deve delegar
    - devolve a resposta pronta

    Ele não deve concentrar toda a lógica da aplicação.
    O ideal é que ele apenas coordene os serviços.

    Exemplo:
    - comando de LED -> envia para LedService
    - comando de motor -> envia para MotorService
    - comando de sensor -> envia para SensorService
    """

    def __init__(self):
        """
        Este método é executado quando criamos uma instância do MachineService.

        Aqui preparamos os services que a máquina vai usar.
        """

        # Cria o serviço de comunicação serial.
        # Esse service será responsável por conversar diretamente com o Arduino.
        self.serial_service = SerialService()

        # Cria o serviço do LED.
        # Repare que passamos o serial_service para ele.
        #
        # Isso acontece porque o LedService precisa enviar comandos
        # para o Arduino através da serial.
        self.led_service = LedService(self.serial_service)

    def handle_command(self, data: dict) -> dict:
        """
        Método principal responsável por interpretar
        os dados recebidos do frontend.

        Recebe um dicionário Python, por exemplo:
        {
            "action": "led_on"
        }

        ou no formato antigo:
        {
            "command": "ON"
        }

        A responsabilidade deste método é:
        1. ler os dados recebidos
        2. identificar qual comando foi enviado
        3. encaminhar para o service correto
        4. devolver a resposta final
        """

        # Tenta pegar o campo "action", que representa o padrão novo do frontend.
        # Exemplo:
        # {"action": "led_on"}
        action = data.get("action")

        # Tenta pegar o campo "command", usado no padrão antigo.
        # Exemplo:
        # {"command": "ON"}
        legacy_command = data.get("command")

        # ============================================================
        # COMPATIBILIDADE COM FRONTEND ANTIGO
        # ============================================================
        #
        # Aqui mantemos suporte ao formato anterior,
        # para evitar quebrar a aplicação enquanto o frontend
        # ainda estiver usando "command" em vez de "action".
        #
        # Exemplo antigo:
        # {"command": "ON"}
        #
        # Isso permite migração gradual do frontend.
        #

        if legacy_command == "ON":
            # Se o frontend antigo mandar ON,
            # delegamos para o LedService ligar o LED.
            return self.led_service.led_on()

        if legacy_command == "OFF":
            # Se o frontend antigo mandar OFF,
            # delegamos para o LedService desligar o LED.
            return self.led_service.led_off()

        # ============================================================
        # NOVO PADRÃO DE COMUNICAÇÃO
        # ============================================================
        #
        # Agora usamos "action", que é mais descritivo
        # e escalável para crescer a aplicação.
        #
        # Exemplo:
        # {"action": "ping"}
        # {"action": "led_on"}
        # {"action": "led_off"}
        #

        if action == "ping":
            # Responde um teste de comunicação simples.
            # Muito útil para verificar se frontend e backend
            # estão se comunicando corretamente.
            return self._handle_ping()

        if action == "led_on":
            # Delega para o serviço de LED a responsabilidade
            # de ligar o LED.
            return self.led_service.led_on()

        if action == "led_off":
            # Delega para o serviço de LED a responsabilidade
            # de desligar o LED.
            return self.led_service.led_off()

        # Se nenhuma ação conhecida for encontrada,
        # devolvemos uma resposta de erro.
        return {
            "type": "error",
            "message": f"Ação inválida: {action or legacy_command}"
        }

    def _handle_ping(self) -> dict:
        """
        Método interno usado para responder testes de conexão.

        O underline (_) no início do nome indica que este método
        é de uso interno da classe.

        Ele é útil quando o frontend quer apenas verificar:
        - se o backend está online
        - se o WebSocket está funcionando
        - se a comunicação está viva
        """
        return {
            "type": "pong",
            "message": "Backend respondeu com sucesso"
        }

    def disconnect(self) -> None:
        """
        Método chamado quando a conexão WebSocket for encerrada.

        Aqui fazemos a limpeza dos recursos utilizados pela máquina.

        Neste caso:
        - fechamos a conexão serial

        Isso é importante para evitar:
        - porta serial presa
        - conexões abertas desnecessariamente
        - problemas ao reconectar depois
        """
        self.serial_service.disconnect()