void setMotorSpeed(int mySpeed){
  if(digitalRead(12) == HIGH){
    analogWrite(motorPin, mySpeed);
  }
  else{
    analogWrite(motorPin, 0);
  }
}

void setMotorSpeed(){
   if(digitalRead(12) == HIGH){
  }
  else{
    analogWrite(motorPin, 0);
  }
  
}
