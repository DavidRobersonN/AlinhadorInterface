class LedService:
    """
    Service responsável apenas pelas ações relacionadas ao LED.

    Ideia principal:
    esta classe não fala diretamente com o frontend
    e nem com o WebSocket.

    O papel dela é:
    - receber uma solicitação
    - mandar o comando correto para a porta serial
    - montar uma resposta organizada
    """

    def __init__(self, serial_service):
        """
        Método construtor da classe.

        O que acontece aqui:
        quando criamos um LedService, precisamos entregar para ele
        um objeto chamado serial_service.

        Esse serial_service é o serviço que sabe se comunicar
        com o Arduino pela porta serial.

        Exemplo mental:
        - LedService = decide o que fazer com o LED
        - SerialService = sabe como enviar o comando para o Arduino
        """
        self.serial_service = serial_service

    def led_on(self) -> dict:
        """
        Método responsável por ligar o LED.

        Fluxo:
        1. envia o comando 'LED_ON' para o Arduino
        2. guarda a resposta em serial_result
        3. devolve um dicionário com as informações da ação realizada
        """

        # Envia o comando para o serviço serial.
        # Aqui estamos dizendo ao Arduino:
        # "ligue o LED"
        serial_result = self.serial_service.send_command("LED_ON")

        # Retorna um dicionário com a resposta padronizada.
        # Esse dicionário pode ser enviado para o frontend.
        return {
            # Tipo da mensagem.
            # Serve para o frontend identificar que essa resposta
            # está relacionada ao estado do LED.
            "type": "led_status",

            # Estado atual esperado do LED após o comando.
            "state": "ON",

            # Mensagem descritiva para log, debug ou interface.
            "message": "Comando para ligar LED enviado com sucesso",

            # Guarda também o resultado retornado pelo SerialService.
            # Isso ajuda a verificar se o envio para o Arduino funcionou.
            "serial": serial_result,
        }

    def led_off(self) -> dict:
        """
        Método responsável por desligar o LED.

        Fluxo:
        1. envia o comando 'LED_OFF' para o Arduino
        2. guarda a resposta em serial_result
        3. devolve um dicionário com as informações da ação realizada
        """
 
        # Envia o comando para o Arduino pedindo para desligar o LED.
        serial_result = self.serial_service.send_command("LED_OFF")

        # Retorna uma resposta padronizada.
        return {
            # Tipo da mensagem para o frontend saber como interpretar.
            "type": "led_status",

            # Estado esperado do LED após o comando.
            "state": "OFF",

            # Mensagem informando o que foi feito.
            "message": "Comando para desligar LED enviado com sucesso",

            # Resultado retornado pela comunicação serial.
            "serial": serial_result,
        }