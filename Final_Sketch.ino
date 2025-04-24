#include "VernierLib.h" //include Vernier functions in this sketch
#include <Servo.h>
VernierLib Vernier; //create an instance of the VernierLib library
float sensorReading;
float Eo = 1;
float S = 26;
const int BUTTON_PIN = 12;
const int SERVO_PIN = 13;

Servo servo;

int angle = 0;
 
void setup() {
  Serial.begin(9600);
  Vernier.autoID(); //identify the sensor being used
  servo.attach(SERVO_PIN);

  servo.write(angle);

}

void loop() {
      angle = 10;

    
    servo.write(angle);


  float E = Vernier.readSensor();
  double result1 = E-Eo;
  double result2 = result1/S;

  double finalResult = pow(10, result2);  // Calculate 10^(x-y/z)
  Serial.print(finalResult);
  Serial.println(" ppm");
  delay(500);//half a second
}
