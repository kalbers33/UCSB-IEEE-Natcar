///Calculates the four possible distances from the input value

void calcDistance(){
  int counter;
  for(counter = 0; counter< numberOfSensors; counter++)
  {
    double usedConstant = kSensorValue[counter]/(2*sData[counter]);
    sDistance[counter][0] = usedConstant + sqrt((usedConstant*usedConstant)-sHeight*sHeight) - sWidth[counter];
    sDistance[counter][1] = usedConstant - sqrt((usedConstant*usedConstant)-sHeight*sHeight) - sWidth[counter];
    sDistance[counter][2] = -(sDistance[counter][1]) - 2*sWidth[counter];
    sDistance[counter][3] = -(sDistance[counter][0]) - 2*sWidth[counter];
  }
}
