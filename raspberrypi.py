import socket

# Configurar servidor
s = socket.socket()
s.bind(("0.0.0.0", 8080))
s.listen(5)

print("Esperando conexión...")

while True:
    conn, addr = s.accept()
    print("Conexión establecida desde:", addr)

    with open('imagen_recibida.jpg', 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    conn.close()
    print("Imagen recibida y guardada como imagen_recibida.jpg")