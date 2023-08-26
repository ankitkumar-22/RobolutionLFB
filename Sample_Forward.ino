// Motor control pins
int enA = 6;
int leftMotorPin1 = 8;
int leftMotorPin2 = 7;
// Motor B connections
int enB = 11;
int rightMotorPin1 = 9;
int rightMotorPin2 = 10;
int speed = 110;



void setup() {
  pinMode(leftMotorPin1, OUTPUT);
  pinMode(leftMotorPin2, OUTPUT);
  pinMode(rightMotorPin1, OUTPUT);
  pinMode(rightMotorPin2, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = (char)Serial.read();
    
    if (command == 'F') {
      // Move forward
      analogWrite(enA,speed);
      analogWrite(enB,speed);
      digitalWrite(leftMotorPin1, HIGH);
      digitalWrite(leftMotorPin2, LOW);
      digitalWrite(rightMotorPin1, HIGH);
      digitalWrite(rightMotorPin2, LOW);
    } else if (command == 'L') {
      // Turn left
      analogWrite(enA,speed);
      analogWrite(enB,50);
      digitalWrite(leftMotorPin1, LOW);
      digitalWrite(leftMotorPin2, HIGH);
      digitalWrite(rightMotorPin1, LOW);
      digitalWrite(rightMotorPin2, LOW);
    } else if (command == 'R') {
      // Turn right
      analogWrite(enA,50);
      analogWrite(enB,speed);
      digitalWrite(leftMotorPin1, LOW);
      digitalWrite(leftMotorPin2, LOW);
      digitalWrite(rightMotorPin1, LOW);
      digitalWrite(rightMotorPin2, HIGH);
    }
  }
}