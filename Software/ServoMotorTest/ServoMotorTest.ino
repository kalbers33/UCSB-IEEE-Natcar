#include <Servo.h>
Servo carDirection;

void setup(){
  Serial.begin(9600);
  pinMode(11, OUTPUT);
  digitalWrite(11, LOW);
  carDirection.attach(9);
  carDirection.write(115); //165 max, 70 min, 115 middle
  //analogWrite(11, 25);
}

void loop(){
  /*
  int i;
  for(i =127; i< 147; i++){
    carDirection.write(i);
    delay(50);
  }
  carDirection.write(107 );
  delay(500);
  for(i =127; i> 107; i--){
    carDirection.write(i);
    delay(50);
  }
  carDirection.write(107);
  delay(500);

*/
}
