#include "MobileRobot.h"
#include "Timer.h"
#include "Parameter.h"

#define ANALOG_PIN A5

float timerMin = 10000;

Timer timerMinControl(timerMin); // timerMin was added in parameter.cpp as 'int Parameter::timerMin = 60000;'


bool label = true;
String datalabel1 = "Time";
String datalabel2 = "Voltage";

int sensorValue; 
float voltage;
unsigned long startTime, actualTime;

//--------------------------- Setup -----------------------------------

void setup() 
{ 

  pinMode(ANALOG_PIN, INPUT);
  Serial.begin(9600); 
  while (!Serial) {}

  delay(1);

  timerMinControl.init();
  
  startTime = millis(); 

}

//--------------------------- Loop -----------------------------------

void loop() {
  
  if(label){// Only run once 
    Serial.print(datalabel1);
    Serial.print(",");
    Serial.println(datalabel2);
    label = false;
  }


  if (timerMinControl.isTime()) {
   
    sensorValue = analogRead(ANALOG_PIN); // Read ther analogic value
    voltage = sensorValue * (5.0 / 1023.0); // Voltage conversion

    actualTime = millis() - startTime; 

    Serial.print(actualTime);
    Serial.print(",");
    Serial.println(voltage);

    sensorValue, voltage = 0;
  }
  
  delay(10);
}
