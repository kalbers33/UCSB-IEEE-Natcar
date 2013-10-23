
#include <math.h>
#include <Servo.h>

//Sensor hight and placement from middle of car in Centimeters
const double sHeight = 4.3;
const double sWidth[] = {-10, -5, 0, 5, 10};
#define numberOfSensors 5

//Constants used for the PID control
#define Kp 0.53; //0.53
const int maxIntegralError = 400; //400
const int dTerms = 1; //1
#define Ki .025 //.025
#define Kd 500; //60

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
int servoDirection = 115;

void setup(){
  pinMode(12, INPUT);
  Serial.begin(9600);
  carDirection.attach(9);
  carDirection.write(servoDirection);
  //Keep car away from magnetic fields when lightis off.
  findMinValue();
  //Rub car across the track when the light is on to find the constant used in calculations. 
  findConstant();
  //digitalWrite(11, 0);
}

void loop(){
  while((millis()%10)!=0);
  getData(); 
  calcDistance(); 
  servoDirection = 115;
  servoDirection -= controlPID();
  if(servoDirection < 70){
    servoDirection = 70;
  }
  if(servoDirection > 170){
    servoDirection = 170;
  }
  carDirection.write(servoDirection);

  int i;
  Serial.print("!");
  int temp = (currentAverageDistance +17)*7;
  Serial.println((char)temp);

 /* for (i = 0; i < numberOfSensors; i++){
    Serial.print(sData[i]);
    Serial.print(" ");
  } */
  if((millis()%100)<50){
    if(currentAverageDistance < 0 && currentAverageDistance > -20){
      digitalWrite(13, 0);
     }
  }else{
    digitalWrite(13,1);
  }
   
  
  
}
