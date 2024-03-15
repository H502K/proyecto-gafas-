#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

class Pantalla:public Stream 
{
private:
  int alto;
  int ancho;
  int i2c;
  int reset;
  Adafruit_SSD1306* panta;

public:
  int i;
  int k;
  Pantalla();
  void inicializar();
  void imprimir();
  void borrar();
  virtual size_t write(uint8_t c);  
  virtual int available();  
  virtual int read();  
  virtual int peek();  
  virtual void flush();  

 
};
