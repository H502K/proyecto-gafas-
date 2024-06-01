import socket
import base64

# Configurar servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 65432))
s.listen()

print("Esperando conexión...")

while True:
    try:
        conn, addr = s.accept()
        print("Conexión establecida desde:", addr)

        conn.send(b'/capture')  # Mensaje de solicitud
        image_data = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            image_data += data #acumula los datos de la imagen
    except:
        pass
    
    #codificacionde la imagen a base 64
    decoded_image = base64.b64decode(image_data)
    
    with open('imagen_recibida.jpg', 'wb') as f:
        f.write(data)

    print("Imagen recibida y guardada como imagen_recibida.jpg")
    #print("Imagen codificada en base 64:", encoded_image_str[:100]) #se muestra los datos de la cadena
