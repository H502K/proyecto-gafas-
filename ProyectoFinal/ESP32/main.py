import network
import socket
from machine import Pin
from time import sleep
#import base64
import ubinascii
import ustruct
import camera
import menup
import Menu
#from menu import Menu 
import _thread

# Configurar conexión WiFi
SSID = 'Redmi Note 9'
PASSWORD = 'fernando'

# Configurar la dirección IP y puerto del servidor
SERVER_IP = '192.168.250.205'
SERVER_PORT = 65432

# Configurar el pin del botón
BUTTON_PIN = 0  #Pin que acciona el boton para dar la orden

# Configurar el botón
button = Pin(BUTTON_PIN, Pin.IN)

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
def connect_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    return s

# Tomar una foto y enviarla al servidor en base 64
def capture_photo():
    print('Solicitando a la ESP32-CAM que tome una foto...')
    s = connect_client()
    request = s.recv(1024)
    if request == b'capture':
        
        #codigo para tomar la foto hace falta
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        camera.framesize(camera.FRAME_VGA)
        buf = camera.capture()    
        camera.deinit()
        
        encoded_image = ubinascii.b2a_base64(buf)
        #encoded_image_str = encoded_image.decode('utf-8')
        
        s.sendall(encoded_image)  # Mensaje de envio
        s.close()
        print('Solicitud enviada con éxito.')
 

#en otro archivo para que no hayan problemas
#captura de audio a traves de i2s
def cam_esp():
    while True:
        capture_photo()

def main():
    connect_wifi()
    while True:
        #logica del menu
        pass
        
        #otro archivo que haga lo del audio
        #i2s = init_i2s()
        #capture_and_send_audio(i2s)
        

if __name__ == '__main__':
    _thread.start_new_thread(cam_esp, ())
    main()