#include <Wire.h>

int RightMotor_E_pin = 5;      // 오른쪽 모터의 Enable & PWM
int LeftMotor_E_pin = 6;       // 왼쪽 모터의 Enable & PWM
int RightMotor_1_pin = 8;      // 오른쪽 모터 제어선 IN1
int RightMotor_2_pin = 9;      // 오른쪽 모터 제어선 IN2
int LeftMotor_3_pin = 10;      // 왼쪽 모터 제어선 IN3
int LeftMotor_4_pin = 11;      // 왼쪽 모터 제어선 IN4

//출력핀(trig)과 입력핀(echo) 설정
int trigPin = 13;                  // 디지털 13번 핀에 연결
int echoPin = 12;                  // 디지털 12번 핀에 연결
int Ultra_d = 0;

int L_Line = A5; // 왼쪽 라인트레이서 센서는 A5 핀에 연결
int C_Line = A4; // 가운데 라인트레이서 센서는 A4 핀에 연결
int R_Line = A3; // 오른쪽 라인트레이서 센서는 A3 핀에 연결

int SC = 0;
int SR = 0;
int SL = 0;

//좌우 모터 속도 조절, 설정 가능 최대 속도 : 255
int L_MotorSpeed = 153; // 왼쪽 모터 속도
int R_MotorSpeed = 153; // 오른쪽 모터 속도

const int myAddress = 0x36;
char receivedData; // 최대 10개의 문자를 저장할 수 있는 배열

// 속도 값들을 배열로 저장
int speeds[] = {30, 40, 50, 60, 70, 80, 90, 100, 110, 255};
const int numSpeeds = sizeof(speeds) / sizeof(speeds[0]);

bool hasReceivedSpeed = false; // 속도 값을 받았는지 여부

void setup() {


  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);

  pinMode(RightMotor_E_pin, OUTPUT);
  pinMode(LeftMotor_E_pin, OUTPUT);
  pinMode(RightMotor_1_pin, OUTPUT);
  pinMode(RightMotor_2_pin, OUTPUT);
  pinMode(LeftMotor_3_pin, OUTPUT);
  pinMode(LeftMotor_4_pin, OUTPUT);

  Serial.begin(9600);
  Wire.begin(myAddress);
  Wire.onReceive(receiveEvent);

}

void loop() {
  int L = digitalRead(L_Line);
  int C = digitalRead(C_Line);
  int R = digitalRead(R_Line);

  if (obstacleDetected()) {
    motorStop();
    Serial.println("Obstacle detected - Stopping motors");
    return; // 함수 종료 후 다음 루프로 넘어감
  }

  int targetSpeed = atoi(receivedData);
  int targetSpeedIndex = -1;

  for (int i = 0; i < numSpeeds; i++) {
      if (targetSpeed == speeds[i]) {
        targetSpeedIndex = i;
        break;
      }
    }

  if (targetSpeedIndex != -1) {
      L_MotorSpeed = speeds[targetSpeedIndex];
      R_MotorSpeed = speeds[targetSpeedIndex];
  } else {
      L_MotorSpeed = 153;
      R_MotorSpeed = 153;
  }

      
  memset(receivedData, 0, sizeof(receivedData));
  hasReceivedSpeed = false;
  lineFollowing(L, C, R);
}

bool obstacleDetected() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  int duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.0343 / 2;

  // 거리가 일정 값 이하인 경우에 장애물로 간주
  if (distance <= 20) {
    return true;
  }
  return false;
}

void lineFollowing(int L, int C, int R) {
  if ( L == LOW && C == LOW && R == LOW ) {           // 0 0 0
    L = SL; C = SC; R = SR;
  }

  if ( L == LOW && C == HIGH && R == LOW ) {          // 0 1 0
    motor_role(HIGH, HIGH);
  }
  
  else if (L == LOW && R == HIGH ){                   // 0 0 1, 0 1 1
    motor_role(LOW, HIGH);
  }
 
  else if (L == HIGH && R == LOW ) {                  // 1 0 0, 1 1 0
    motor_role(HIGH, LOW);
  }
  else if ( L == HIGH && R == HIGH ) {                // 1 1 1, 1 0 1
    motorStop();
  }
  SL = L; SC = C; SR = R;
}

void motor_role(int R_motor, int L_motor) {
  digitalWrite(RightMotor_1_pin, R_motor);
  digitalWrite(RightMotor_2_pin, !R_motor);
  digitalWrite(LeftMotor_3_pin, L_motor);
  digitalWrite(LeftMotor_4_pin, !L_motor);
  analogWrite(RightMotor_E_pin, R_MotorSpeed);  
  analogWrite(LeftMotor_E_pin, L_MotorSpeed);  
}

void motorStop() {
  analogWrite(RightMotor_E_pin, 0);
  analogWrite(LeftMotor_E_pin, 0);
}

void receiveEvent(int bytes) {
  while (Wire.available()) {
    char c = Wire.read();
    receivedData = c;
  }
}
