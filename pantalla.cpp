#include "pantalla.h"

Pantalla::Pantalla() 
{
  //caracteristicas de la pantalla, se uso una de 0.96"
  ancho=128;
  alto=64;
  i2c=0x3c;
  reset=-1;
  
  k=1;
  i=0; 
}

void Pantalla::inicializar()
{
  panta = new Adafruit_SSD1306(ancho, alto, &Wire, reset);
  panta->begin(SSD1306_SWITCHCAPVCC, i2c);
  panta->clearDisplay();
  panta->setTextColor(WHITE);
}

void Pantalla::imprimir()
{ 
  panta->setTextSize(2);
  panta->setCursor(15, 20);
  //panta->setCursor(15, 10 + i * 15);  
  //i++;
  if(i==3)
  {i=0;}
}

void Pantalla::borrar()
{
  panta->clearDisplay(); 
  //panta->setCursor(15, 10 + i * 15);  

}


size_t Pantalla::write(uint8_t c) {
  panta->write(c);
  panta->display();

  return 1;
}

int Pantalla::available() {}

int Pantalla::read() {}

int Pantalla::peek() {}

void Pantalla::flush() {}
