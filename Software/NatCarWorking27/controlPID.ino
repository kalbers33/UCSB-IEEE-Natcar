double controlPID(){
  static double integral_err;
  static double delta_error[3];
  static int dCount;
  
  double error;
  double p_out = 0;
  double i_out = 0;
  double d_out = 0;
  double output = 0;
  error = currentAverageDistance;
  delta_error[dCount++] = currentAverageDistance - oldAverageDistance;
  if(dCount > 2) dCount = 0;
  if(abs(integral_err + error) < maxIntegralError){
  integral_err += error;
  }
  
  p_out = error*Kp;
  i_out = integral_err*Ki;
  int i;
  for(i = 0; i <3; i++){
    d_out = delta_error[i]*Kd;
  }
  if(d_out > 35) d_out = 35;
  if(d_out < -35) d_out = -35;
  
  output = p_out + i_out + d_out;
  
  if(output > 47){
    output = 47;
  }
  if(output < -47){
    output = -47;
  }
  return output;
}
  
  
  
  
