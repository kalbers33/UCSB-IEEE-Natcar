// State machine
const unsigned int IDLE_STATE = 0;
const unsigned int CALIBRATE_STATE = 1;
const unsigned int RUN_STATE = 2;
const unsigned int ERR_STATE = 65535;
// Current state
unsigned int CURRENT_STATE = IDLE_STATE;

// state button
const unsigned int STATE_BUTTON = PUSH1;

// state button sensing
boolean PREV_STATE_BUTTON = false;

void setup()
{
  // put your setup code here, to run once:
  
  // LED status lights
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  
  // Buttons for controlling car
  pinMode(STATE_BUTTON, INPUT_PULLUP); // switch state
  
  pinMode(PF_2, OUTPUT);
  
  // set state just to be safe :)
  CURRENT_STATE = IDLE_STATE;
}

void loop()
{
  
  // deal with user buttons
  boolean stateButtonSwitched = false;
  boolean currButtonState = !digitalRead(STATE_BUTTON);
  if (PREV_STATE_BUTTON == false && currButtonState == true) {
    stateButtonSwitched = true;
  }
  PREV_STATE_BUTTON = currButtonState;
  
  if (CURRENT_STATE == IDLE_STATE) {
    // IDLE STATE
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    //digitalWrite(BLUE_LED, LOW);
    analogWrite(PF_2, 0);
    // State transistion
    if (stateButtonSwitched) {
      CURRENT_STATE = RUN_STATE;
    }
  } else if (CURRENT_STATE == CALIBRATE_STATE) {
    // calibrating mode
    digitalWrite(BLUE_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);
  } else if (CURRENT_STATE == RUN_STATE) {
    // run through course
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, HIGH);
    //digitalWrite(BLUE_LED, HIGH);
    
    analogWrite(PF_2, 64);
    
    // state transition
    if (stateButtonSwitched) {
      CURRENT_STATE = IDLE_STATE;
    }
  } else if (CURRENT_STATE == ERR_STATE) {
    // error! I need help
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(BLUE_LED, LOW);
  } else {
    // Shouldn't be here
  }
  
  // delay for stability
  delay(1);
}
