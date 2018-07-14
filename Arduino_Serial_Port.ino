/*******************************
Author:          Harsh Gosar (harshgosar0@gmail.com)
Description:     To test ublox LEA 6H GPS module 
Created Date:    12-MAY-2018
Version:         1.0
Supported board: Arduino UNO, Mega 2560 or board that supports hardware serial ports
********************************/
void setup() {
  Serial.begin(9600);   // connect Tx/Rx of GPS to Rx(pin 0)/Tx(pin 1) of Arduino 
  while (!Serial) {}    // wait for serial port to connect. Needed for native USB port only
}

void loop() {
  //check if serial port have any data
  if (Serial.available()) {
    String response = "";
      while (Serial.available()) {
        char inByte = Serial.read();
        response += inByte; // cast char bytes into string
      }
    Serial.print(response);
  }
}
