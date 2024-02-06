// Created: 2019-04-02 16:00:00
#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial BT(0,1);    // Definimos los pines RX y TX del Arduino conectados al Bluetooth
const int trigPin = 10;  // Pin TRIG conectado al pin 9
const int echoPin = 11; // Pin ECHO conectado al pin 10
const int servoPin = 9; // Pin del servo
// Define la variable para almacenar la distancia
float distancia;
const int count = 6;

Servo servo;

void setup()
{
  BT.begin(9600);       // Inicializamos el puerto serie BT (Para Modo AT 2)
  Serial.begin(9600);   // Inicializamos  el puerto serie  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
    pinMode(servoPin, OUTPUT);
  for (size_t i = 2; i < count; i++)
  {
    pinMode(i, OUTPUT);
  }
  servo.attach(servoPin);
  
}
 
void loop()
{
 if(BT.available())    // Si llega un dato por el puerto BT se envía al monitor serial
  {
    Serial.write(BT.read());
  }
 
  if(Serial.available())  // Si llega un dato por el monitor serial se envía al puerto BT
  {
     BT.write(Serial.read());
  }
}


void medir_distancia(){
    digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Mide el tiempo que tarda en recibir el eco
  distancia = pulseIn(echoPin, HIGH) * 0.0343 / 2;

  // Imprime la distancia medida en el puerto serie
delay(200);


  return distancia;

  // Espera un tiempo antes de realizar la próxima medición
}

void mover_servo(int angulo){
  servo.write(angulo);
}