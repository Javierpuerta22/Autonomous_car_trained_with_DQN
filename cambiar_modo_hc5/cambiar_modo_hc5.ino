/*
 * Changing HC05 module's default device name using AT Command
 * by Droiduino.cc
 *
 * Pinout:
 * Key --> pin 9
 * VCC --> Vin
 * TXD --> pin 10
 * RXD --> pin 11
 * GND --> GND
 *
 * AT Command : AT+NAME=
 *
 */
 
#include "SoftwareSerial.h"
#include <Servo.h>

const int trigPin = 6;  // Pin TRIG conectado al pin 9
const int echoPin = 7; // Pin ECHO conectado al pin 10
const int servoPin = 9; // Pin del 
const int count = 6;
String pos;
int e = 8;
int angulo = 0;
bool incrementando = true;
SoftwareSerial bluetooth(10, 11);   // RX | TX
Servo servo;
void setup()
{

  Serial.begin(9600);
  bluetooth.begin(9600);  // HC-05 default speed in AT command mode
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
    pinMode(servoPin, OUTPUT);
    pinMode(12, OUTPUT);

    pinMode(2, OUTPUT);
      pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);

  servo.attach(servoPin);
  servo.write(angulo);
}
 
void loop()
{
 if (bluetooth.available()>= 1) {
    // Si hay datos disponibles en el módulo Bluetooth, leelos y envíalos de vuelta
     pos = bluetooth.readString();
      e= pos.toInt();
      select_action(e);
    delay(15);
  }

  int distancia = medir_distancia();
  int angulo = mover_servo();
  servo.write(angulo);
  bluetooth.println(String(distancia) + "," + String(angulo));
  delay(200);
}

void select_action(int valor){
  if (valor == 0){
    IZQUIERDA();
  }
  else if (valor == 1){
    DERECHA();
  }
  else if (valor == 2){
    ADELANTE();
  }
  else if (valor == 3){
    ATRAS();
  }
}

int mover_servo(){
  if (incrementando) {
    angulo += 10; // Incrementa el ángulo
    
    // Si el ángulo alcanza los 180 grados, cambia la dirección a decrementar
    if (angulo >= 150) {
      angulo = 150; // Asegura que el ángulo no exceda 180
      incrementando = false; // Cambia la dirección a decrementar
    }
    return angulo;
  }
  // Si estamos decrementando el ángulo
  else {
    angulo -= 10; // Decrementa el ángulo

    // Si el ángulo alcanza los 0 grados, cambia la dirección a incrementar
    if (angulo <= 0) {
      angulo = 0; // Asegura que el ángulo no sea menor que 0
      incrementando = true; // Cambia la dirección a incrementar
    }
    return angulo;
  }
}

void ATRAS(){
  digitalWrite(2, LOW);
 digitalWrite(3, LOW);
   digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}
void DERECHA(){
  digitalWrite(2, HIGH);
 digitalWrite(3, HIGH);
   digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
}

void IZQUIERDA(){
  digitalWrite(2, HIGH);
 digitalWrite(3, HIGH);
   digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
}

void ADELANTE(){
  digitalWrite(2, HIGH);
 digitalWrite(3, HIGH);
   digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}

int medir_distancia(){
    digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Mide el tiempo que tarda en recibir el eco
  int distancia = pulseIn(echoPin, HIGH) * 0.0343 / 2;
  // Imprime la distancia medida en el puerto serie
  return distancia;
  
  // Espera un tiempo antes de realizar la próxima medición
}
