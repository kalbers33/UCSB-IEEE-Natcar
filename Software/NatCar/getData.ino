//Get data from all sensors

void getData(){
  int counter = 0;
  for( counter = 0; counter < numberOfSensors; counter++){
    sData[counter] = analogRead(counter);
  }
}
