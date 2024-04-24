import sensor
import image
import uos
import network
import socket

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.run(1)

# Conección a la red wifi
ssid = "Redmi Note 9"
password = "fernando"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    pass

print("Conexión establecida. IP:", wifi.ifconfig()[0])

img = sensor.snapshot()

nombre_archivo = '/imagen.jpg'
with open(nombre_archivo, 'w') as f:
    img.save(f)

s = socket.socket()
s.connect(("197.184.18.0.1", 8080))

with open(nombre_archivo, 'rb') as f:
    data = f.read(1024)
    while data:
        s.send(data)
        data = f.read(1024)

s.close()

print("Imagen enviada a la Raspberry Pi")