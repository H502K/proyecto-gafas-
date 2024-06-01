from flask import Flask, request
from flask import render_template
import socket
import wave

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 65432)

try:
    server_socket.bind(server_address)
    server_socket.listen()
    print(f"Servidor escuchando en {server_address}")
except Exception as e:
    print(f"Error al iniciar el servidor: {e}")
    exit()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.post('/update_led')
def updateLed():
    data = request.get_json()
    led_status = data.get('ledStatus', 'off')
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")
        if led_status == 'on':
            client_socket.sendall(b'1')
        else:
            client_socket.sendall(b'0')
        #client_socket.close()
        return {'response': 'ok'}
    except Exception as e:
        print(f"Error al enviar datos al cliente: {e}")
        return {'response': 'error'}

@app.post('/ESP32_CONECT')
def esp32Conect():
    if esp32.is_open:
        return {'response': 'ESP32 conectada'}
    else:
        return {'response': 'ESP32 no conectada'}

@app.post('/capture')
def capture_photo():
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")
        client_socket.sendall(b'capture')
        image_data = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            image_data += data
        return {'response': image_data}
    except Exception as e:
        print(f"Error al capturar la foto: {e}")
        return {'response': 'Error al capturar la foto'}

@app.post('/capture_audio')
def capture_audio():
    try:
        with wave.open('static/audio_recibido.wav', 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes que serian 16 bits
            wf.setframerate(16000)

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                wf.writeframes(data)

        
        return {'response': 'Audio capturado y guardado.'}
    except:
        return {'response': f'Error al capturar el audio.'}

if __name__ == "__main__":
    app.run(debug=False, host = '0.0.0.0')