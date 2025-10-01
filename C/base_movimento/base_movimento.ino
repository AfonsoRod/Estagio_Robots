

#include <MeMCore.h>

MeDCMotor motor1(M1); //motor esquerda
MeDCMotor motor2(M2); //motor direita
MeUltrasonicSensor ultrasonic(PORT_3); //sensor distancia
int list_dir[4];


void frente(){
  motor1.run(-100);
  motor2.run(100);
  delay(1600);
  motor1.run(0);
  motor2.run(0); 
}
void tras(){
  motor1.run(100);
  motor2.run(-100);
  delay(1600);
  motor1.run(0);
  motor2.run(0);

}
void esquerda(){
  motor1.run(100);
  motor2.run(100);
  
  delay(800); // ajusta o tempo até dar 90º

  // Parar os motores
  motor1.run(0);
  motor2.run(0);
}
void direita(){
  motor1.run(-100);
  motor2.run(-100); // trás

  delay(800); // ajusta o tempo até dar 90º

  // Parar os motores
  motor1.run(0);
  motor2.run(0);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    
    switch (cmd) {
      case 'f':  // frente
        frente();
        break;
      case 'b':  // trás
        tras();
        break;
      case 'l':  // virar à esquerda
        esquerda();
        break;
      case 'r':  // virar à direita
        direita();
        break;
      case 'z':  // rodar sentido horário
        motor1.run(-100);
        motor2.run(-100);
        break;
      case 'x':  // rodar sentido anti-horário
        motor1.run(100);
        motor2.run(100);
        break;
      case 's':  // parar
        motor1.run(0);
        motor2.run(0);
        break;
      case 'v':
        scan_360();
        break;
    
    }
  }
}


void scan_360(){
  for (int i = 0; i < 4; i++) {
    verificar_distancia(i);
    direita();
    delay(800);
    //Serial.print(list_dir[i]);
  }
  enviar_leituras();
}
void verificar_distancia(int i){
  long distance = ultrasonic.distanceCm();
  list_dir[i] = distance;
  //Serial.print(distance);
}
void enviar_leituras(){
  for (int i = 0;i< 4; i++){
    if(i== 3){
      Serial.println(list_dir[i]);
    }
    else{
      Serial.print(list_dir[i]);
      Serial.print(",");}
    
  }

}