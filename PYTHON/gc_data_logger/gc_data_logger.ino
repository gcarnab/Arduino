const int potPin = A6; // Pin analogico collegato al potenziometro
const int buttonPin = 8;

void setup() {
  Serial.begin(9600); // Inizializza la comunicazione seriale
  pinMode(buttonPin, INPUT_PULLUP);  // Pin 8 reads 1 if not connected to GND
  pinMode(LED_BUILTIN, OUTPUT); // We can now use the built in LED  
}

void loop() {
  // Leggi il valore dal potenziometro
  int potValue = analogRead(potPin);
  bool buttonPressed = !digitalRead(buttonPin);

  if(buttonPressed){
    // Invia il valore via seriale
    Serial.println(potValue);
  }

  digitalWrite(LED_BUILTIN, buttonPressed);

  delay(100); // Ritardo per stabilizzare le letture
}
