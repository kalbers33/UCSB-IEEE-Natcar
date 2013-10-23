//Get data from all sensors

void getData(){
  int counter = 0;
  int times;
  for( times = 0; times < numberOfSensors; times++){
     sData[times] = 0;
  }
  for( times = 0; times < 10; times++){
    for( counter = 0; counter < numberOfSensors; counter++){
      sData[counter] += analogRead(counter) - sensorMinValue[counter];
    }
  }
  for(counter = 0; counter < numberOfSensors; counter++){
    sData[counter] /= 10;
  }
}
