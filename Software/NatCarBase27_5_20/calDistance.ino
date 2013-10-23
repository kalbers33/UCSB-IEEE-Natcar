//Calculates all the possible distances from the input value, finds out which ones are correct and averages them. 
//After testing on our car this seemed to be accurate to about half a centimeter, but usually more accurate. 
//Diagonal distance was measured parallel to the sensor middle acces, not perpendicular to the wire as I expected. This should not be too much of an issue. 

void calcDistance(){
  int counter;
  int badValues = 0;
  oldAverageDistance = currentAverageDistance;
  currentAverageDistance = 0;
  const int throwAway = 6; //Throw away distance values less than this number when averaging
  //Serial.println();
  for(counter = 0; counter < numberOfSensors; counter++){
    if(sData[counter] < 3){         //Another Threshold value that can be edited
      sDistance[counter] = 27;
    }else{
      sDistance[counter] = sqrt(max((kSensorValue[counter]*sHeight/sData[counter] - sHeight*sHeight), 0));
    }
    //Serial.print(sDistance[counter]);
    //Serial.print(" ");
  }
  for(counter = 0; counter< numberOfSensors; counter++)
  {
    if(sDistance[counter] >= throwAway){
      badValues++;
      continue;
    }
    if ((counter < (numberOfSensors - 1)) && (counter > 0) ){
      if(sDistance[counter  - 1] > sDistance[counter + 1]){
        currentAverageDistance += sDistance[counter] + sWidth[counter];
      }
      else{
        currentAverageDistance += -sDistance[counter] + sWidth[counter];
      }
    }
    else if(counter == 0){
      if(sDistance[counter + 1] < 5.0){
        currentAverageDistance += sDistance[counter]+ sWidth[counter];
      }
      else{
        currentAverageDistance += -sDistance[counter] + sWidth[counter];
      }
    }
    else if(counter == (numberOfSensors - 1)){
      if(sDistance[counter - 1] > 5.0 ){
        currentAverageDistance += sDistance[counter] + sWidth[counter];
      }
      else{
        currentAverageDistance += -sDistance[counter] + sWidth[counter];
      }
    }
  }
  if(badValues == numberOfSensors && oldAverageDistance < 0){
    currentAverageDistance = -10.00 - throwAway - 1;
  }else if(badValues == numberOfSensors && oldAverageDistance > 0){
    currentAverageDistance = 10.00 + throwAway + 1;
  }else{
  currentAverageDistance = currentAverageDistance/(numberOfSensors-badValues);
  }
}
