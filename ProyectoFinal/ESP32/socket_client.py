#Socket esp32

import socket

# Configurar la dirección IP y puerto del cliente (ESP32-CAM)
CLIENT_IP = '192.168.250.205'
CLIENT_PORT = 65432

# Configurar y conectar el socket al cliente
def connect_client():
    s = socket.socket()
    s.connect((CLIENT_IP, CLIENT_PORT))
    return s

# Solicitar al cliente que tome y envíe la foto
def capture_photo():
    print('Solicitando a la ESP32-CAM que tome una foto...')
    s = connect_client()
    request = s.recv(1024)
    if request == b'capture':
        
        encoded_image = base64.b64encode(request)
        encoded_image_str = encoded_image.decode('utf-8')
        
        s.sendall(data)  # Mensaje de solicitud
        s.close()
        print('Solicitud enviada con éxito.')

# Función principal
def main():
    request_photo()

if __name__ == '__main__':
    main()