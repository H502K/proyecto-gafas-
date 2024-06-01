import network
import socket
from machine import Pin, I2C
from time import sleep, ticks_ms, time
import ubinascii
import camera
import ssd1306
import random
import ustruct
import urequests as requests
import pygame  # Importar pygame para manejo de audio
import _thread

# Configurar conexión WiFi
SSID = 'Redmi Note 9'
PASSWORD = 'fernando'

# Configurar la dirección IP y puerto del servidor
SERVER_IP = '192.168.250.205'
SERVER_PORT = 65432

# Configurar el pin del botón para captura de fotos
PHOTO_BUTTON_PIN = 0  # Pin que acciona el botón para capturar foto
photo_button = Pin(PHOTO_BUTTON_PIN, Pin.IN)

# Inicialización de la pantalla OLED
i2c = I2C(0, scl=Pin(12), sda=Pin(13))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.show()

# Clase para el menú
class Menu:
    def __init__(self):
        self.items = []
        self.index = 0
        self.in_submenu = False

    def add_item(self, text, action):
        self.items.append((text, action))

    def Up(self):
        if self.in_submenu:
            return
        self.index = (self.index - 1) % len(self.items)
        self.display_current_option()

    def down(self):
        if self.in_submenu:
            return
        self.index = (self.index + 1) % len(self.items)
        self.display_current_option()

    def enter(self):
        if self.in_submenu:
            self.in_submenu = False
            self.display_current_option()
        else:
            self.in_submenu = True
            _, action = self.items[self.index]
            action()

    def display_current_option(self):
        oled.fill(0)
        for i, item in enumerate(self.items):
            prefix = ">" if i == self.index else " "
            oled.text(f"{prefix} {item[0]}", 0, i * 10)
        oled.show()

menu = Menu()

# Definición de las funciones de las opciones del menú
def opcion0():
    grados = random.randint(0, 40)
    texto = "{}C".format(grados)
    oled.fill(0)
    oled.text('Temp:', 0, 0)
    oled.text(texto, 0, 16)
    oled.show()

def opcion1():
    tiempo_transcurrido = int(time())
    horas = tiempo_transcurrido // 3600
    minutos = (tiempo_transcurrido % 3600) // 60
    segundos = tiempo_transcurrido % 60
    tiempo_formateado = "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos)
    oled.fill(0)
    oled.text('Cronómetro:', 0, 0)
    oled.text(tiempo_formateado, 0, 16)
    oled.show()

def obtener_hora():
    try:
        URL = "https://timeapi.io/api/Time/current/zone"
        response = requests.get(URL + '?timeZone=America/Bogota')
        response.raise_for_status()  # Check for HTTP errors
        hora = response.json().get('dateTime', 'No data')
        oled.fill(0)
        oled.text('Hora actual:', 0, 0)
        oled.text(hora[:16], 0, 16)  # Display the first part of the datetime
        oled.show()
    except Exception as e:
        oled.fill(0)
        oled.text('Error al', 0, 0)
        oled.text('obtener hora', 0, 16)
        oled.show()
        print(e)

def obtener_dolar():
    try:
        URL = "https://dolarapi.com/v1/dolares"
        response = requests.get(URL)
        response.raise_for_status()  # Check for HTTP errors
        dolar_compra = response.json()[0].get('compra', 'No data')
        oled.fill(0)
        oled.text('Dolar compra:', 0, 0)
        oled.text(str(dolar_compra), 0, 16)
        oled.show()
    except Exception as e:
        oled.fill(0)
        oled.text('Error al', 0, 0)
        oled.text('obtener dolar', 0, 16)
        oled.show()
        print(e)

# Configuración de los parámetros de la API de OpenAI
ENDPOINT_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "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"

headers = {
    "Authorization": "Bearer " + API_KEY,
    "Content-type": "application/json"
}

def getAnswer(question):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": "En un párrafo de no más de 40 palabras, " + question
            }
        ]
    }

    response = requests.post(ENDPOINT_URL, json=data, headers=headers)
    result = response.json()['choices'][0]['message']['content']

    print(result)
    return result

def chatgpt():
    try:
        from audio_nuevo import TTS
        from stt import SpeechtoText

        tts = TTS()
        speech = SpeechtoText()

        ret, text = speech.getText()
        if ret:
            print('El texto es: ', text)
            result = getAnswer(text)
            oled.fill(0)
            oled.text('ChatGPT:', 0, 0)
            oled.text(result[:20], 0, 16)
            oled.text(result[20:40], 0, 26)
            oled.show()
            tts.playText(result)
        else:
            oled.fill(0)
            oled.text('Error:', 0, 0)
            oled.text(text, 0, 16)
            oled.show()
            print('Error: ', text)
    except Exception as e:
        oled.fill(0)
        oled.text('Error al', 0, 0)
        oled.text('preguntar', 0, 16)
        oled.show()
        print(e)

# Añadir las opciones al menú
menu.add_item("Temperatura", opcion0)
menu.add_item("Cronometro", opcion1)
menu.add_item("Hora Actual", obtener_hora)
menu.add_item("Dolar Compra", obtener_dolar)
menu.add_item("Preguntar a ChatGPT", chatgpt)

# Inicialización de los pines para los LEDs y botones
led1 = Pin(5, Pin.OUT)
led2 = Pin(15, Pin.OUT)

btnUp = Pin(4, Pin.IN, Pin.PULL_UP)
btndown = Pin(2, Pin.IN, Pin.PULL_UP)
btnenter = Pin(14, Pin.IN, Pin.PULL_UP)

# Variables para controlar el tiempo entre pulsaciones de botones
last_time = 0
debounce_time = 200  # Tiempo de rebote en milisegundos

# Función para manejar las interrupciones de botones
def button_handler(pin):
    global last_time
    current_time = ticks_ms()
    if current_time - last_time >= debounce_time:
        if pin == btnUp:
            menu.Up()
        elif pin == btndown:
            menu.down()
        elif pin == btnenter:
            menu.enter()
        last_time = current_time

# Configurar las interrupciones de botones
btnUp.irq(handler=button_handler, trigger=Pin.IRQ_FALLING)
btndown.irq(handler=button_handler, trigger=Pin.IRQ_FALLING)
btnenter.irq(handler=button_handler, trigger=Pin.IRQ_FALLING)

# Mostrar el menú inicial
menu.display_current_option()

while True:
    pass  # Mantener el programa corriendo para las interrupciones

# Conectar a la red WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Conexión Wi-Fi exitosa. IP:', wlan.ifconfig()[0])

# Configurar y conectar el socket al servidor
def connect_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    return s

# Tomar una foto y enviarla al servidor en base64
def capture_photo():
    print('Solicitando a la ESP32-CAM que tome una foto...')
    s = connect_server()
    
    s.sendall(b'capture')  # Enviar solicitud de captura de foto
    response = s.recv(1024)
    
    if response == b'ready':
        # Inicializar y capturar la foto
        camera.init(0, format=camera.JPEG, fb)
