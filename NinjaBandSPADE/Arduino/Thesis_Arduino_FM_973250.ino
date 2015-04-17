#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();
int LDR_Pin = A0; //analog pin 0
int L0=6; //Light 0 connected to pin 6
int L1=11; //Light 1 connected to pin 11
int L2=3; //Light 2 connected to pin 3
int L3=9; //Light 3 connected to pin 9
long Timer;

void setup() {
  Serial.begin(9600);
  mySwitch.enableReceive(0);  // Receiver on inerrupt 0 => that is pin #2
  mySwitch.enableTransmit(4);   // Transmitter is connected to Arduino Pin #4  
  pinMode(L0,OUTPUT); //Pin is set to output
  pinMode(L1,OUTPUT); //Pin is set to output
  pinMode(L2,OUTPUT); //Pin is set to output
  pinMode(L3,OUTPUT); //Pin is set to output
}

void loop() {
  int LDRReading = analogRead(LDR_Pin);  //Get value from the photoresistor

  if  (LDRReading < 100) mySwitch.send("000000000000001111101000"); //Send value over RF433
  if  (LDRReading >= 100 && LDRReading < 200) mySwitch.send("000000000000010001001100"); //Send value over RF433
  if  (LDRReading >= 200 && LDRReading < 300) mySwitch.send("000000000000010010110000"); //Send value over RF433
  if  (LDRReading >= 300 && LDRReading < 400) mySwitch.send("000000000000010100010100"); //Send value over RF433
  if  (LDRReading >= 400 && LDRReading < 500) mySwitch.send("000000000000010101111000"); //Send value over RF433
  if  (LDRReading >= 500 && LDRReading < 600) mySwitch.send("000000000000010111011100"); //Send value over RF433
  if  (LDRReading >= 600 && LDRReading < 700) mySwitch.send("000000000000011001000000"); //Send value over RF433
  if  (LDRReading >= 700 && LDRReading < 800) mySwitch.send("000000000000011010100100"); //Send value over RF433
  if  (LDRReading >= 800 && LDRReading < 900) mySwitch.send("000000000000011100001000"); //Send value over RF433
  if  (LDRReading >= 900 && LDRReading < 1000) mySwitch.send("000000000000011101101100"); //Send value over RF433
  if  (LDRReading >= 1000) mySwitch.send("000000000000011111010000"); //Send value over RF433

  Timer = millis()+5000;
  while (millis()<Timer){
    if (mySwitch.available()) {
      int mult;
      int value = mySwitch.getReceivedValue()*mult;
      mult=1;
      if (value == 0) {
        Serial.print("Unknown encoding");
      } 
      else {
        Serial.print("Received ");
        Serial.print( mySwitch.getReceivedValue() );
        Serial.print(" / ");
        Serial.print( mySwitch.getReceivedBitlength() );
        Serial.print("bit ");
        Serial.print("Protocol: ");
        Serial.println( mySwitch.getReceivedProtocol() );
        if (mySwitch.getReceivedValue() == 500002) {
          analogWrite(L0, 100); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500003) {
          analogWrite(L1, 100); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500004) {
          analogWrite(L2, 100); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500005) {
          analogWrite(L3, 25); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500006) {
          analogWrite(L3, 50); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500007) {
          analogWrite(L3, 75); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else if (mySwitch.getReceivedValue() == 500008) {
          analogWrite(L3, 100); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
        else  {
          analogWrite(L0, 0); // By changing values from 0 to 255 you can change the amount of light
          analogWrite(L1, 0); // By changing values from 0 to 255 you can change the amount of light
          analogWrite(L2, 0); // By changing values from 0 to 255 you can change the amount of light
          analogWrite(L3, 0); // By changing values from 0 to 255 you can change the amount of light
          mult=0;
        }
      }
      //Zero conf investigar cero configuracion

      mySwitch.resetAvailable();
    }  
  }  
}


