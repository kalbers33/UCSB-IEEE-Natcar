void setup(){
  int sData[5];
  Serial.begin(9600);
}
void loop(){
  int i;
  for(i = 0; i < 5; i++){
    Serial.print(analogRead(i));
    Serial.print(" ");
  }
  delay(100);
  Serial.println();
}
    
