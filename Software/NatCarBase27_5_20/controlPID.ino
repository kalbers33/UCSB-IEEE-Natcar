double controlPID(){
  static double integral_err;
  static double delta_error[dTerms];
  static int dCount;
  
  double error;
  double p_out = 0;
  double i_out = 0;
  double d_out = 0;
  double output = 0;
  error = currentAverageDistance;
  delta_error[dCount++] = (currentAverageDistance - oldAverageDistance);
  if(dCount >= dTerms) dCount = 0;
  if(abs(integral_err + error) < maxIntegralError){
  integral_err += error;
  }
  if((error < 5 )&& (error > -5)) integral_err /= 2;
  p_out = error*abs(error)*Kp;
  i_out = integral_err*Ki;
  
  //if(d_out > 35) d_out = 35;
  //if(d_out < -35) d_out = -35;
  int i;
  for(i = 0; i <dTerms; i++){
    d_out = delta_error[i]*Kd;
  }
  
  output = p_out + i_out + d_out;
  
  if(abs(error) < 10){
    setMotorSpeed(24);
  }else{
    setMotorSpeed(20);
  }
  
  /*if(output > 47){
    output = 47;
  }
  if(output < -47){
    output = -47;
  }*/
  return output;
}
  
  
  
  
