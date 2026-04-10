import threading
import time
from typing import Optional

import serial


class SerialService:
    """
    Responsável pela comunicação com o Arduino via porta serial.

    Esta classe apenas envia e lê comandos.
    Ela não decide regras de LED, motor ou interface.
    """

    def __init__(
        self,
        port: str = "COM6",
        baudrate: int = 9600,
        timeout: float = 1.0
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self._serial: Optional[serial.Serial] = None
        self._lock = threading.Lock()

    def connect(self) -> bool:
        """
        Tenta abrir a conexão serial.
        Retorna True se conectar com sucesso.
        """
        if self.is_connected():
            return True

        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )

            # Aguarda o Arduino reiniciar após abrir a serial
            time.sleep(2)
            return True

        except Exception:
            self._serial = None
            return False

    def is_connected(self) -> bool:
        """
        Verifica se a serial está conectada e aberta.
        """
        return self._serial is not None and self._serial.is_open

    def disconnect(self) -> None:
        """
        Fecha a conexão serial, se estiver aberta.
        """
        try:
            if self._serial and self._serial.is_open:
                self._serial.close()
        finally:
            self._serial = None

    def send_command(self, command: str) -> dict:
        """
        Envia um comando de texto puro para o Arduino.
        Exemplo: LED_ON, LED_OFF, LED_TOGGLE
        """
        if not self.is_connected():
            connected = self.connect()
            if not connected:
                raise Exception("Não foi possível conectar à serial.")

        try:
            if not command.endswith("\n"):
                command += "\n"

            with self._lock:
                if self._serial is None:
                    raise Exception("Serial não inicializada.")

                self._serial.write(command.encode("utf-8"))
                self._serial.flush()

            return {
                "success": True,
                "command_sent": command.strip()
            }

        except Exception as error:
            self.disconnect()
            raise Exception(f"Erro ao enviar comando serial: {error}")

    def read_line(self) -> Optional[str]:
        """
        Lê uma linha da serial.
        Retorna string ou None.
        """
        if not self.is_connected():
            connected = self.connect()
            if not connected:
                return None

        try:
            with self._lock:
                if self._serial is None:
                    return None

                line = self._serial.readline().decode("utf-8", errors="ignore").strip()

            return line if line else None

        except Exception:
            self.disconnect()
            return None