# Importa o módulo threading, usado para trabalhar com travas (lock)
# e evitar que duas partes do sistema acessem a serial ao mesmo tempo.
import threading

# Importa o módulo time para usar pausas no código, como time.sleep().
import time

# Importa Optional do typing.
# Optional[str], por exemplo, significa que o retorno pode ser uma string ou None.
from typing import Optional

# Importa a biblioteca pyserial, responsável pela comunicação serial com o Arduino.
import serial


# Define a classe SerialService.
# Ela centraliza toda a comunicação com a porta serial.
class SerialService:
    """
    Responsável pela comunicação com o Arduino via porta serial.

    Esta classe apenas envia e lê comandos.
    Ela não decide regras de LED, motor ou interface.
    """

    # Método construtor da classe.
    # Ele é chamado automaticamente quando fazemos:
    # serial_service = SerialService()
    def __init__(
        self,
        port: str = "COM9",         # Porta serial padrão onde o Arduino está conectado.
        baudrate: int = 9600,       # Velocidade de comunicação serial.
        timeout: float = 1.0        # Tempo máximo de espera para leitura da serial.
    ):
        # Salva a porta recebida como atributo da instância.
        self.port = port

        # Salva o baudrate recebido como atributo da instância.
        self.baudrate = baudrate

        # Salva o timeout recebido como atributo da instância.
        self.timeout = timeout

        # Inicializa o atributo _serial com None.
        # Depois, quando conectar, esse atributo passará a guardar o objeto serial.Serial.
        self._serial: Optional[serial.Serial] = None

        # Cria um lock para proteger o acesso concorrente à porta serial.
        # Isso evita problemas caso múltiplas threads tentem escrever/ler ao mesmo tempo.
        self._lock = threading.Lock()

    # Método responsável por abrir a conexão serial.
    def connect(self) -> bool:
        """
        Tenta abrir a conexão serial.
        Retorna True se conectar com sucesso.
        """

        # Se já estiver conectado, não precisa reconectar.
        # Retorna True imediatamente.
        if self.is_connected():
            return True

        try:
            # Cria o objeto de conexão serial com os parâmetros configurados.
            self._serial = serial.Serial(
                port=self.port,            # Porta COM utilizada.
                baudrate=self.baudrate,    # Velocidade da comunicação.
                timeout=self.timeout       # Tempo limite de leitura.
            )

            # Aguarda 2 segundos após abrir a serial.
            # Isso é importante porque muitos Arduinos reiniciam ao abrir a conexão serial.
            time.sleep(2)

            # Se chegou até aqui, a conexão deu certo.
            return True

        except Exception:
            # Se ocorrer erro ao conectar, garante que _serial volte para None.
            self._serial = None

            # Retorna False para indicar falha na conexão.
            return False

    # Método que verifica se a serial está aberta e pronta para uso.
    def is_connected(self) -> bool:
        """
        Verifica se a serial está conectada e aberta.
        """

        # Retorna True somente se:
        # 1. self._serial não for None
        # 2. a porta estiver aberta (is_open == True)
        return self._serial is not None and self._serial.is_open

    # Método responsável por fechar a conexão serial.
    def disconnect(self) -> None:
        """
        Fecha a conexão serial, se estiver aberta.
        """
        try:
            # Verifica se existe um objeto serial e se ele está aberto.
            if self._serial and self._serial.is_open:
                # Fecha a conexão serial.
                self._serial.close()
        finally:
            # Independentemente de erro ou não, limpa a referência do objeto serial.
            self._serial = None

    # Método responsável por enviar um comando para o Arduino.
    def send_command(self, command: str) -> dict:
        """
        Envia um comando de texto puro para o Arduino.
        Exemplo: LED_ON, LED_OFF, LED_TOGGLE
        """

        # Antes de enviar, verifica se a serial está conectada.
        if not self.is_connected():
            # Tenta conectar automaticamente caso não esteja conectado.
            connected = self.connect()

            # Se não conseguir conectar, lança uma exceção.
            if not connected:
                raise Exception("Não foi possível conectar à serial.")

        try:
            # Garante que o comando termine com quebra de linha.
            # Isso é importante porque o Arduino normalmente lê comandos por linha.
            if not command.endswith("\n"):
                command += "\n"

            # Usa um lock para garantir acesso exclusivo à serial durante a escrita.
            with self._lock:
                # Confirma novamente se a serial existe.
                if self._serial is None:
                    raise Exception("Serial não inicializada.")

                # Converte a string para bytes em UTF-8 e envia para a serial.
                self._serial.write(command.encode("utf-8"))
                # Força o envio imediato do buffer de escrita.
                self._serial.flush()

            # Retorna um dicionário informando sucesso no envio.
            return {
                "success": True,
                "command_sent": command.strip()  # strip() remove o \n para exibir limpo.
            }

        except Exception as error:
            # Em caso de erro durante o envio, desconecta a serial por segurança.
            self.disconnect()

            # Lança uma nova exceção com uma mensagem mais clara.
            raise Exception(f"Erro ao enviar comando serial: {error}")

    # Método responsável por ler uma linha da serial.
    def read_line(self) -> Optional[str]:
        """
        Lê uma linha da serial.
        Retorna string ou None.
        """

        # Se não estiver conectado, tenta conectar automaticamente.
        if not self.is_connected():
            connected = self.connect()

            # Se não conseguir conectar, retorna None.
            if not connected:
                return None

        try:
            # Usa lock para evitar conflito com outras leituras/escritas simultâneas.
            with self._lock:
                # Se o objeto serial não existir, retorna None.
                if self._serial is None:
                    return None

                # Lê uma linha da serial até encontrar '\n' ou até o timeout expirar.
                # decode converte bytes para string.
                # errors="ignore" ignora caracteres inválidos.
                # strip remove espaços e quebras de linha extras.
                line = self._serial.readline().decode("utf-8", errors="ignore").strip()

            # Se a linha tiver conteúdo, retorna a string.
            # Se vier vazia, retorna None.
            return line if line else None

        except Exception:
            # Em caso de erro na leitura, desconecta por segurança.
            self.disconnect()

            # Retorna None para indicar falha ou ausência de leitura.
            return None
        

    def send_command_and_read(self, command: str) -> dict:
        """
        Envia um comando para o Arduino e lê a resposta imediatamente,
        tudo dentro do mesmo lock para evitar concorrência.
        """

        if not self.is_connected():
            connected = self.connect()
            if not connected:
                return {
                    "success": False,
                    "error": "Não foi possível conectar à serial.",
                }

        try:
            if not command.endswith("\n"):
                command += "\n"

            with self._lock:
                if self._serial is None:
                    return {
                        "success": False,
                        "error": "Serial não inicializada.",
                    }


                self._serial.write(command.encode("utf-8"))
                self._serial.flush()

                response = self._serial.readline().decode("utf-8", errors="ignore").strip()

                return {
                    "success": True,
                    "command_sent": command.strip(),
                    "response": response,
                }

        except Exception as error:
            self.disconnect()
            return {
                "success": False,
                "error": str(error),
            }        