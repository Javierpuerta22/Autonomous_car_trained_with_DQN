// Created: 2019-04-02 16:00:00
#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial BT(0,1);    // Definimos los pines RX y TX del Arduino conectados al Bluetooth
const int trigPin = 6;  // Pin TRIG conectado al pin 9
const int echoPin = 7; // Pin ECHO conectado al pin 10
const int servoPin = 9; // Pin del servo
// Define la variable para almacenar la distancia
float distancia;
const int count = 6;
Servo servo;

void setup()
{
  BT.begin(9600);       // Inicializamos el puerto serie BT (Para Modo AT 2)
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
    pinMode(servoPin, OUTPUT);
    pinMode(12, OUTPUT);
  for (size_t i = 2; i < count; i++)
  {
    pinMode(i, OUTPUT);
  }
  servo.attach(servoPin);
}
 
void loop()
{

if (BT.available() > 0) {
    char receive = BT.read();
    if(receive == '1') //If received data is 1, turn on the LED and send back the sensor data
    {
      digitalWrite(12, HIGH); 
      BT.println("Encendido correctamente");
    }
    else digitalWrite(12, LOW);//If received other data, turn off LED
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

  // Espera un tiempo antes de realizar la próxima medición
}

void mover_servo(int angulo){
  servo.write(angulo);
}
