
//Sensor hight and placement from middle of car in Centimeters
#define sHeight 3
#define sWidth0 -5
#define sWidth1 -3
#define sWidth2 0
#define sWidth3 3
#define sWidth4 5

#define numberOfSensors 5

//Sensor raw data, and calculated k to used for each one
int sData[numberOfSensors]; 
double sWidth[]={-5, -3, 0, 3, 5};
double kSensorValue[numberOfSensors]; 

//Stores measured distance from wire to center of car, each sensor will have 4 possible values
double sDistance[numberOfSensors][4];

double currentAverageDistance;
double oldAverageDistance;

double carDistance; 


void setup(){
  //Rub car across wire to find ax sensor value


}

void loop(){
  
}
