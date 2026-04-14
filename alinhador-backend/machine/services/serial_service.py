import logging
import threading
import time
from typing import Optional

import serial


# Cria um logger para registrar mensagens no terminal,
# como tentativas de conexão, erros e comandos enviados.
logger = logging.getLogger(__name__)


class SerialService:
    """
    Responsável pela comunicação com o Arduino via porta serial.

    Esta classe cuida apenas da comunicação:
    - conectar
    - desconectar
    - enviar comandos
    - ler respostas

    Ela NÃO decide a regra de negócio.
    Exemplo:
    - ela não decide quando ligar LED
    - ela não decide como o motor deve girar
    - ela não decide nada da interface

    O papel dela é apenas conversar com o hardware.
    """

    def __init__(
        self,
        port: str = "COM7",
        baudrate: int = 9600,
        timeout: float = 1.0,
        retry_interval: float = 2.0,
    ):
        """
        Método executado quando a classe é criada.

        Aqui definimos as configurações principais da conexão serial.
        """

        # Porta COM onde o Arduino está conectado no Windows.
        self.port = port

        # Velocidade da comunicação serial.
        # Precisa ser a mesma definida no Arduino.
        self.baudrate = baudrate

        # Tempo limite para operações de leitura.
        # Se passar desse tempo sem resposta, a leitura encerra.
        self.timeout = timeout

        # Tempo de espera entre tentativas de reconexão automática.
        self.retry_interval = retry_interval

        # Guarda o objeto real da conexão serial.
        # Começa como None porque ainda não estamos conectados.
        self._serial: Optional[serial.Serial] = None

        # Lock usado para evitar que duas partes do programa
        # tentem acessar a serial ao mesmo tempo.
        #
        # Isso é MUITO importante, porque a porta serial é um recurso único.
        self._lock = threading.Lock()

        # Controle da thread de reconexão automática.
        self._running = False

        # Guarda a referência da thread de conexão automática.
        self._connection_thread: Optional[threading.Thread] = None

    def start_auto_connect(self) -> None:
        """
        Inicia uma thread em background que fica tentando conectar
        na serial até conseguir.

        Isso é útil quando:
        - o Arduino ainda não está conectado
        - a porta serial caiu
        - você quer que o sistema tente reconectar sozinho
        """

        # Se o loop já estiver rodando, não inicia outro.
        if self._running:
            logger.info("Loop de conexão serial já está em execução.")
            return

        # Marca que o loop está ativo.
        self._running = True

        # Cria uma thread separada para tentar conexão em paralelo,
        # sem travar a aplicação principal.
        self._connection_thread = threading.Thread(
            target=self._auto_connect_loop,
            name="serial-auto-connect",
            daemon=True,
        )

        # Inicia a thread.
        self._connection_thread.start()
        logger.info("Thread de auto conexão serial iniciada.")

    def stop_auto_connect(self) -> None:
        """
        Para o loop de auto conexão.
        """
        self._running = False
        logger.info("Loop de auto conexão serial finalizado.")

    def _auto_connect_loop(self) -> None:
        """
        Loop interno que tenta conectar na serial repetidamente
        enquanto o serviço estiver ativo.

        Ele roda em background.
        """

        while self._running:
            # Se já estiver conectado, apenas espera um pouco
            # antes de verificar novamente.
            if self.is_connected():
                time.sleep(1)
                continue

            logger.info(
                "Tentando conectar na porta serial %s com baudrate %s...",
                self.port,
                self.baudrate,
            )

            # Tenta abrir a conexão.
            connected = self.connect()

            if connected:
                logger.info(
                    "Arduino conectado com sucesso na porta %s.",
                    self.port,
                )
                time.sleep(1)
            else:
                logger.warning(
                    "Falha ao conectar na serial %s. Nova tentativa em %.1f segundo(s).",
                    self.port,
                    self.retry_interval,
                )
                time.sleep(self.retry_interval)

    def connect(self) -> bool:
        """
        Tenta abrir a conexão serial.
        Retorna True se conectar com sucesso.
        Retorna False se falhar.
        """

        # Se já estiver conectado, não tenta abrir outra vez.
        if self.is_connected():
            logger.info("Arduino já está conectado na porta %s.", self.port)
            return True

        try:
            logger.info(
                "Abrindo conexão serial na porta %s com baudrate %s...",
                self.port,
                self.baudrate,
            )

            # Cria a conexão serial real com a porta COM.
            serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )

            # Pequena pausa porque muitos Arduinos reiniciam
            # quando a porta serial é aberta.
            #
            # Sem essa pausa, você pode tentar enviar comando
            # antes do Arduino estar pronto.
            time.sleep(2)

            # Usa lock para garantir segurança ao alterar o estado interno.
            with self._lock:
                self._serial = serial_connection

            logger.info("Conexão serial aberta com sucesso na porta %s.", self.port)
            return True

        except Exception as error:
            # Se der erro, garantimos que a serial fique como None.
            with self._lock:
                self._serial = None

            logger.warning(
                "Erro ao conectar na serial %s: %s",
                self.port,
                error,
            )
            return False

    def is_connected(self) -> bool:
        """
        Verifica se a serial está conectada e aberta.

        Retorna True se:
        - existir objeto serial
        - a porta estiver aberta
        """
        with self._lock:
            return self._serial is not None and self._serial.is_open

    def disconnect(self) -> None:
        """
        Fecha a conexão serial, se estiver aberta.
        """

        with self._lock:
            try:
                # Se existir conexão e ela estiver aberta, fecha.
                if self._serial and self._serial.is_open:
                    self._serial.close()
                    logger.info("Conexão serial fechada.")
            finally:
                # Mesmo que algo dê errado, limpamos a referência.
                self._serial = None

    def send_command(self, command: str) -> dict:
        """
        Envia um comando de texto puro para o Arduino.

        Exemplo:
        - LED_ON
        - LED_OFF
        - MOTOR_LEFT
        - MOTOR_RIGHT

        Esse método apenas envia o comando.
        Ele não lê a resposta do Arduino.
        """

        # Se não estiver conectado, tenta conectar antes de enviar.
        if not self.is_connected():
            connected = self.connect()

            if not connected:
                raise Exception("Não foi possível conectar à serial.")

        try:
            # Garante quebra de linha no final do comando.
            # Isso é comum porque o Arduino geralmente lê linha por linha.
            if not command.endswith("\n"):
                command += "\n"

            with self._lock:
                # Verificação extra de segurança.
                if self._serial is None:
                    raise Exception("Serial não inicializada.")

                # Envia o comando em bytes pela serial.
                self._serial.write(command.encode("utf-8"))

                # Força o envio imediato.
                self._serial.flush()

            logger.info("Comando enviado para serial: %s", command.strip())

            # Retorna uma resposta simples indicando sucesso.
            return {
                "success": True,
                "command_sent": command.strip(),
            }

        except Exception as error:
            logger.warning("Erro ao enviar comando para serial: %s", error)

            # Se algo deu errado, desconecta para evitar estado inconsistente.
            self.disconnect()

            raise Exception(f"Erro ao enviar comando serial: {error}")

    def read_line(self) -> Optional[str]:
        """
        Lê uma linha da serial.

        Retorna:
        - uma string, se conseguiu ler algo
        - None, se não recebeu nada ou se houve erro
        """

        # Se não estiver conectado, tenta conectar antes.
        if not self.is_connected():
            connected = self.connect()

            if not connected:
                return None

        try:
            with self._lock:
                if self._serial is None:
                    return None

                # Lê uma linha da serial, converte de bytes para texto
                # e remove espaços/quebra de linha das pontas.
                line = self._serial.readline().decode("utf-8", errors="ignore").strip()
                print(f"SerialService: Linha lida pelo readLine da serial Vindo do Arduino: '{line}'")  # Log para depuração

            if line:
                logger.info("Linha recebida da serial: %s", line)

            # Retorna a linha se tiver conteúdo.
            # Se vier vazia, retorna None.
            return line if line else None

        except Exception as error:
            logger.warning("Erro ao ler da serial: %s", error)
            self.disconnect()
            return None

    def send_command_and_read(self, command: str) -> dict:
        """
        Envia um comando para o Arduino e lê a resposta imediatamente,
        tudo dentro do mesmo lock para evitar concorrência.

        Esse método é útil quando:
        - você manda um comando
        - e espera uma resposta instantânea do Arduino

        Exemplo:
        comando -> "LED_STATUS"
        resposta -> "ON"
        """

        # Se não estiver conectado, tenta conectar antes.
        if not self.is_connected():
            connected = self.connect()
            if not connected:
                return {
                    "success": False,
                    "error": "Não foi possível conectar à serial.",
                }

        try:
            # Garante quebra de linha no final.
            if not command.endswith("\n"):
                command += "\n"

            with self._lock:
                if self._serial is None:
                    return {
                        "success": False,
                        "error": "Serial não inicializada.",
                    }

                # Envia o comando.
                self._serial.write(command.encode("utf-8"))
                self._serial.flush()

                # Lê imediatamente a resposta do Arduino.
                response = self._serial.readline().decode("utf-8", errors="ignore").strip()

            logger.info(
                "Comando enviado: %s | Resposta recebida: %s",
                command.strip(),
                response,
            )

            return {
                "success": True,
                "command_sent": command.strip(),
                "response": response,
            }

        except Exception as error:
            logger.warning("Erro no send_command_and_read: %s", error)
            self.disconnect()
            return {
                "success": False,
                "error": str(error),
            }


# Instância pronta para ser reutilizada em outros pontos do projeto,
# se você quiser trabalhar com um objeto único de SerialService.
serial_service = SerialService()
