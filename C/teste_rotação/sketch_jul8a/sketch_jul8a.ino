
#include <MeMCore.h>

MeDCMotor motor1(M1); //motor esquerda
MeDCMotor motor2(M2); //motor direita
MeUltrasonicSensor ultrasonic(PORT_3); //sensor distancia
 int list_dir[4];

void verificar_distancia(int i){
  long distance = ultrasonic.distanceCm();
  list_dir[i] = distance;
  Serial.print(distance);
}

void virar_direita(){
  motor1.run(-100);
  motor2.run(-100); // trás

  delay(800); // ajusta o tempo até dar 90º

  // Parar os motores
  motor1.run(0);
  motor2.run(0);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i < 4; i++) {
    virar_direita();
    verificar_distancia(i);
    delay(800);
    //Serial.print(list_dir[i]);

  }
 Serial.print("\n");
  Serial.print("finalizou");
  for(int j=0 ; j<4; j++){
      Serial.print(list_dir[j]);
      Serial.print(",");

  }

}

void loop() {
  // put your main code here, to run repeatedly:

}
