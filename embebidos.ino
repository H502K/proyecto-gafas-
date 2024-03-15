#include "menu.h"
#include "pantalla.h"

#define LED0 19
#define LED1 18
#define LED2 5

Menu menu;
Pantalla pantalla;

hw_timer_t *timer = NULL;
hw_timer_t *timer1 = NULL;
hw_timer_t *timer2 = NULL;

volatile unsigned long lastTime=0;
volatile boolean bUp, bDown, bEnter;
volatile boolean bOption0 = true;
volatile boolean bOption1 = true;
volatile boolean bOption2 = true;
volatile boolean bCuenta, bHora, bDia;
volatile unsigned long startTime=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pantalla.inicializar();
  menu.begin(pantalla);
  
  
  menu.addItem("option 0", option0);
  menu.addItem("option 1", option1);
  menu.addItem("option 2", option2);

  pinMode(LED0, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  pinMode(14, INPUT_PULLUP);
  pinMode(26, INPUT_PULLUP);
  pinMode(27, INPUT_PULLUP);

  attachInterrupt(14, enter, FALLING);
  attachInterrupt(26, subir, FALLING);
  attachInterrupt(27, bajar, FALLING);

  bUp = bDown = bEnter = false;
  bCuenta = bHora = bDia = false;

  timer = timerBegin(0, 80, true);

  timerAttachInterrupt(timer, cuenta, true);
  timerAlarmWrite(timer, 1000000, true);
  timerAlarmEnable(timer);
  
  timerRestart(timer);
  timerStart(timer);
  timerStop(timer);

  timer1 = timerBegin(0, 80, true);

  timerAttachInterrupt(timer1, hora, true);
  timerAlarmWrite(timer1, 1000000, true);
  timerAlarmEnable(timer1);
  
  timerRestart(timer1);
  timerStart(timer1);
  timerStop(timer1);


  timer2 = timerBegin(0, 80, true);

  timerAttachInterrupt(timer2, dia, true);
  timerAlarmWrite(timer2, 1000000, true);
  timerAlarmEnable(timer2);
  
  timerRestart(timer2);
  timerStart(timer2);
  timerStop(timer2);

}

void loop() {
  // put your main code here, to run repeatedly:
  int Boton1 = digitalRead(14);
  int Boton2 = digitalRead(26);
  int Boton3 = digitalRead(27);

  if (bEnter==true)
  {
  pantalla.borrar();
  pantalla.inicializar();
  menu.enter();
  bEnter = false;
  }
  if (bUp==true)
  {
  pantalla.borrar();
  pantalla.imprimir();
  menu.up();
  bUp = false;
  }
  if (bDown==true)
  {
  pantalla.borrar();
  pantalla.imprimir();
  menu.down();
  bDown = false;
  }
  if(bCuenta==true){
    pantalla.borrar();
    pantalla.imprimir();
    iniciarcuenta();
    bCuenta=false;
  }
  if(bHora==true){
    pantalla.borrar();
    pantalla.imprimir();
    iniciarhora();
    bHora=false;
  }
  if(bDia==true){
    pantalla.borrar();
    pantalla.imprimir();
    iniciardia();
    bDia=false;
  }
  delay(1000);
}

void ARDUINO_ISR_ATTR cuenta() 
{
  //digitalWrite(LED0, !digitalRead(LED0));
  bCuenta = true;
}

void ARDUINO_ISR_ATTR hora() 
{
  //digitalWrite(LED0, !digitalRead(LED0));
  bHora = true;
}

void ARDUINO_ISR_ATTR dia() 
{
  //digitalWrite(LED0, !digitalRead(LED0));
  bDia = true;
}

void ARDUINO_ISR_ATTR enter(){
  if((millis()-lastTime>50)){
  //pantalla.inicializar();
  //menu.enter();
  bEnter = true;
  lastTime=millis();
  }
  }

void ARDUINO_ISR_ATTR  subir(){
  if((millis()-lastTime>50)){
  //pantalla.imprimir();
  //menu.up();
  bUp = true;
  lastTime=millis();
  }
  }

void ARDUINO_ISR_ATTR  bajar(){
  if((millis()-lastTime>50)){
  //pantalla.imprimir();
  bDown = true;
  //menu.down();
  lastTime=millis();
  }
  }

void option0()
{
  if(bOption0) {
    timerRestart(timer);
    timerStart(timer);
    cuenta();
  }  else {
    timerStop(timer);
  }

  bOption0 = !bOption0;
}

void option1()
{
  if(bOption1) {
    timerRestart(timer1);
    timerStart(timer1);
    hora();
  }  else {
    timerStop(timer1);
  }

  bOption1 = !bOption1;
}

void option2()
{
  if(bOption2) {
    timerRestart(timer2);
    timerStart(timer2);
    dia();
  }  else {
    timerStop(timer2);
  }

  bOption2 = !bOption2;
}

void iniciarcuenta(){
  pantalla.println("cuenta: ");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("1");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("2");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("3");
}

void iniciarhora(){
  pantalla.imprimir();
  pantalla.println("Hora: ");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("12:00");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("1:00");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("2:00");
}

void iniciardia(){
  pantalla.println("Dia: ");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("Lunes");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("Martes");
  pantalla.borrar();
  pantalla.imprimir();
  pantalla.println("Miercoles");
}
