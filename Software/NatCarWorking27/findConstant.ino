//Finds the constants used to calculate distance later for each sensor, depending on the max value sensed. 

void findConstant(){
  int counter;
  int countPin;
  int currentK = 0;
  digitalWrite(13, 1);
  for(counter = 0; counter < 500; counter++){
    for(countPin = 0; countPin < numberOfSensors; countPin++){
      currentK = analogRead(countPin);
      if(currentK > kSensorValue[countPin]){
        kSensorValue[countPin] = currentK;
      }
    }
    delay(10);

  }
  for(counter = 0; counter < numberOfSensors; counter++){
    kSensorValue[counter] = (kSensorValue[counter] - sensorMinValue[counter])*sHeight;
  }

}
