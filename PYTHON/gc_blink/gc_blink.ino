const int ledPin = 13;  // Pin connected to the LED

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);  // Set the baud rate to match Python script
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the command from Python

    if (command == '1') {
      digitalWrite(ledPin, HIGH);  // Turn on the LED
    } else if (command == '0') {
      digitalWrite(ledPin, LOW);  // Turn off the LED
    }
  }
}

