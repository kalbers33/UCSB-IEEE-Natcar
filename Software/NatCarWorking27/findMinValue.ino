//Finds the minimun Value that the sensors read when no magenetic field is arround, this must be done with the sensors far away from any magnetic field 

void findMinValue(){
  int counter;
  int countPin;
  for (counter = 0; counter < 500; counter++){
    for(countPin = 0; countPin < numberOfSensors; countPin++){
      sensorMinValue[countPin] += analogRead(countPin);
    }
    delay(10);
  }
  for(countPin = 0; countPin < numberOfSensors; countPin++){
    sensorMinValue[countPin] /= 500;
  }  
}
    
