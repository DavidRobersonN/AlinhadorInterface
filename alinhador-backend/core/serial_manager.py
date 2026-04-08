import threading
import serial
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

SERIAL_PORT = 'COM3'   # troque depois para a porta correta
BAUD_RATE = 9600

arduino = None


def connect_to_arduino():
    global arduino
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f'Conectado ao Arduino em {SERIAL_PORT}')
    except Exception as e:
        arduino = None
        print(f'Arduino não conectado: {e}')


def send_command_to_arduino(command):
    global arduino
    if arduino and arduino.is_open:
        arduino.write((command + '\n').encode())
    else:
        print(f'Comando "{command}" não enviado: Arduino desconectado')


def listen_to_arduino():
    global arduino
    channel_layer = get_channel_layer()

    while True:
        try:
            if arduino and arduino.is_open and arduino.in_waiting > 0:
                line = arduino.readline().decode().strip()

                if line == 'LED_ON':
                    async_to_sync(channel_layer.group_send)(
                        'led_group',
                        {
                            'type': 'led_status',
                            'state': 'ON'
                        }
                    )

                elif line == 'LED_OFF':
                    async_to_sync(channel_layer.group_send)(
                        'led_group',
                        {
                            'type': 'led_status',
                            'state': 'OFF'
                        }
                    )

        except Exception as e:
            print(f'Erro lendo serial: {e}')


def start_serial_listener():
    connect_to_arduino()

    if arduino and arduino.is_open:
        thread = threading.Thread(target=listen_to_arduino, daemon=True)
        thread.start()