/*
Sensor Ultrassônico HC-SR04
Fábio dos Reis
www.bosontreinamentos.com.br 
Edição equipe top*/
#include <Servo.h>
// Definir os números dos pinos
const int trigger = 13;
const int eco = 12;
const int trigger2 = 8;
const int eco2 = 7;
// Definir as variáveis
long duracao;
long duracao2;
float volume;
float dist;
int status_vermelho=0;
int pos = 0;//angulo do servo motor
Servo servo_9;


void setup() {
 servo_9.attach(9);
 pinMode(trigger, OUTPUT); // Configura o pino trigger como saída
 pinMode(eco, INPUT); // Configura o pino eco como entrada.
 pinMode(trigger2, OUTPUT); // Configura o pino trigger como saída
 pinMode(eco2, INPUT); // Configura o pino eco como entrada.
 Serial.begin(9600); // Inicia a comunicação serial
}

void loop() {
 // Limpa o trigger
 digitalWrite(trigger, LOW);
 digitalWrite(trigger2, LOW);
 delayMicroseconds(5);

 // Configurar o trigger para nível alto para transmissão de sinais
 digitalWrite(trigger, HIGH);
  
 delayMicroseconds(10); // tempo para envio do sinal 1
 digitalWrite(trigger, LOW);
 duracao = pulseIn(eco, HIGH);
  ////PROXIMA LEITURA
  
 digitalWrite(trigger2, HIGH); 
 delayMicroseconds(10); // tempo para envio do sinal 2
 digitalWrite(trigger2, LOW);
 // Inicia contagem de tempo e lê o pino de eco
 duracao2 = pulseIn(eco2, HIGH);

 // Calcular a distância
 volume = duracao2 * 0.034 / 2;
 dist = duracao * 0.034 / 2;
 

 // Mostrar a distância no monitor serial
 

 Serial.print("Distancia em cm: ");
 Serial.println(dist);
 Serial.print("Volume em cm: ");
 Serial.println(volume);
  
 if (dist <= 15 && volume < 23) {
 	for (pos = 0; pos <= 90; pos += 90) {//abre a tampa
    	servo_9.write(pos);
    	delay(4000); // Wait for 15 millisecond(s)
     	}
  	for (pos = 90; pos >= 0; pos -= 90) {//fecha a tampa
    	servo_9.write(pos);
    	delay(1000); // Wait for 15 millisecond(s)
    	}
   	Serial.print("houve abertura");
 }

 if (status_vermelho==1 && volume >= 23) {
   Serial.print("Cheio");   
 }
 if ( status_vermelho==0&& volume >= 23) {
   status_vermelho=1;
   Serial.print("Encheu");
 }
 // Aguardar 100ms antes da próxima leitura para evitar interferência
 delay(2000);
}
