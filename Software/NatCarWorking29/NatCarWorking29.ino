
#include <math.h>
#include <Servo.h>

//Sensor hight and placement from middle of car in Centimeters
const double sHeight = 1.6;
const double sWidth[] = {-10, -5, 0, 5, 10};
#define numberOfSensors 5

//Constants used for the PID control
#define Kp 2.5; //2.2
const int maxIntegralError = 200;
#define Ki .025 //.025
#define Kd 65; // 55

#define motorPin 11
#define servoPin 9


//Sensor raw data, and calculated k to used for each one
long sData[numberOfSensors]; 
double kSensorValue[numberOfSensors]; 
long sensorMinValue[numberOfSensors]; //Used to find zero value since this is at an unknown voltage

//Stores measured distance from wire to center of car, each sensor will have 4 possible values
double sDistance[numberOfSensors];

double currentAverageDistance;
double oldAverageDistance;

double carDistance; //Averages the distances found. 

Servo carDirection;
int servoDirection = 107;

void setup(){
  pinMode(12, INPUT);
  //Serial.begin(9600);
  carDirection.attach(9);
  carDirection.write(servoDirection);
  //Keep car away from magnetic fields when lightis off.
  findMinValue();
  //Rub car across the track when the light is on to find the constant used in calculations. 
  findConstant();
  setMotorSpeed(29);
  //digitalWrite(11, 0);
}

void loop(){
  while((millis()%10)!=0);
  getData(); 
  calcDistance(); 
  servoDirection = 107;
  servoDirection += controlPID();
  if(servoDirection < 60){
    servoDirection = 60;
  }
  if(servoDirection > 154){
    servoDirection = 154;
  }
  carDirection.write(servoDirection);

  int i;
  /*Serial.println();
  Serial.println(currentAverageDistance);
  Serial.print("!");
  for (i = 0; i < numberOfSensors; i++){
    Serial.print(sData[i]);
    Serial.print(" ");
  } */
  setMotorSpeed(29);
  if((millis()%100)<50){
    if(currentAverageDistance < 0 && currentAverageDistance > -20){
      digitalWrite(13, 0);
     }
  }else{
    digitalWrite(13,1);
  }
   
  
  
}
