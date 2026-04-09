import threading
import time
import serial
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

SERIAL_PORT = 'COM8'
BAUD_RATE = 9600

arduino = None
listener_started = False


def connect_to_arduino():
    global arduino

    # Se já está conectado, não faz nada
    if arduino and arduino.is_open:
        return True

    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        # Muitos Arduinos reiniciam quando a porta serial é aberta.
        # Esse pequeno atraso ajuda a estabilizar.
        time.sleep(2)

        print(f'Conectado ao Arduino em {SERIAL_PORT}')
        return True

    except Exception as e:
        arduino = None
        print(f'Arduino não conectado: {e}')
        return False


def send_command_to_arduino(command):
    global arduino

    # Se não estiver conectado, tenta reconectar na hora do envio
    if not arduino or not arduino.is_open:
        print('Arduino desconectado. Tentando reconectar...')
        if not connect_to_arduino():
            print(f'Comando "{command}" não enviado: não foi possível reconectar ao Arduino')
            return

    try:
        arduino.write((command + '\n').encode())
        print(f'Comando enviado ao Arduino: {command}')
    except Exception as e:
        print(f'Erro ao enviar comando "{command}": {e}')
        arduino = None


def listen_to_arduino():
    global arduino
    channel_layer = get_channel_layer()

    while True:
        try:
            # Se perdeu a conexão, tenta reconectar sozinho
            if not arduino or not arduino.is_open:
                connect_to_arduino()
                time.sleep(1)
                continue

            if arduino.in_waiting > 0:
                line = arduino.readline().decode(errors='ignore').strip()
                print(f'Recebido do Arduino: {line}')

                if line == 'LED:ON':
                    async_to_sync(channel_layer.group_send)(
                        'led_group',
                        {
                            'type': 'led_status',
                            'state': 'ON'
                        }
                    )

                elif line == 'LED:OFF':
                    async_to_sync(channel_layer.group_send)(
                        'led_group',
                        {
                            'type': 'led_status',
                            'state': 'OFF'
                        }
                    )

            time.sleep(0.05)

        except Exception as e:
            print(f'Erro lendo serial: {e}')
            arduino = None
            time.sleep(1)


def start_serial_listener():
    global listener_started

    # Evita subir duas threads sem querer
    if listener_started:
        return

    listener_started = True

    # Tenta conectar ao iniciar
    connect_to_arduino()

    thread = threading.Thread(target=listen_to_arduino, daemon=True)
    thread.start()