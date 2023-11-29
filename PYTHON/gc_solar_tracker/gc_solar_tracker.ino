//=====> GC LIGHT FOLLOWER <=====//

// #include <Servo.h>
#define ledPin 13
// #define servoPin 6
#define leftSensorPin A0
#define rightSensorPin A1
// Servo myServo;
//const int leftSensorPin = A0; // Pin analogico della fotoresistenza sinistra
//const int rightSensorPin = A1;// Pin analogico della fotoresistenza destra

int diffLight;
int angle;
int sensorValue1;
int sensorValue2;
// necessarie per taratura
int sensorLow = 1023; // Arduino uno risoluzione 10bit = 1024 (0-1023)
int sensorHigh = 0;
//int servoPosition; // not used


void setup() {
    Serial.begin(9600);
    pinMode(ledPin, OUTPUT);

    // TARATURA DEL SISTEMA
    digitalWrite(ledPin, HIGH);
    //Serial.println("Calibrating sensors...");
    while (millis() < 5000)
    { 
        // myServo.Attach(servoPin); // Collega il servomotore al pin specificato
        sensorValue1 = analogRead(leftSensorPin);
        sensorValue2 = analogRead(rightSensorPin);

        if (sensorValue1 > sensorHigh)
        {
            sensorHigh = sensorValue1;
        }
        if (sensorValue1 < sensorLow)
        {
            sensorLow = sensorValue1;
        }
        if (sensorValue2 > sensorHigh)
        {
            sensorHigh = sensorValue2;
        }
        if (sensorValue2 < sensorLow)
        {
            sensorLow = sensorValue2;
        }
        digitalWrite(ledPin, LOW);
    }
    //Serial.println("Calibration complete!");
}

void loop() {
  sensorValue1 = analogRead(leftSensorPin);
  sensorValue2 = analogRead(rightSensorPin);
  // Calcola la differenza tra i valori delle due fotocellule
  diffLight = sensorValue1 - sensorValue2;
  //servoPosition = myServo.read();
  angle = map(diffLight, -1,70,0,179);
  //angle = map(diffLight, -1023, 1023, 0, 180);
  angle = constrain(angle, 0, 180);


  // Invia i dati via seriale a Python
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.print(sensorValue2);
  Serial.print(",");
  Serial.print(diffLight);
  Serial.print(",");
  Serial.println(angle);

  delay(50);
}
