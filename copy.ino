#include <X9C.h>

// --------------- PINS X9C ------------------- //
#define UD  12
#define INC 13
#define CS  11
X9C pot;
// ---------------------------------------------//

//int g = A0;
//int s = A1;
//int a = A2;
//int offset = A3;
//int ads = A5;

int g = A11;
int s = A1;
int a = A2;
int offset = A0;
int ads = A3;


void setup() {
Serial.begin(9600);
pot.begin (CS, INC, UD);
pot.setPot(50, true); // define o potenciometro para metade do whiper
delay(500);
Serial.println("Time;Vg;Vs;Va;Voffset;Vads;/n"); // /n para nao ficar "," e nao causar incoerencias com o script
delay(1000);
}

void loop() {
for (int z=0;z<NC;z++){ //number of cycles 
pot.setPot(50, true); // define o potenciometro para metade do whiper
delay(500);
for (int i=0 ; i<NS; i++){ //number of steps
float t=millis();
pot.trimPot(1, X9C_DOWN, true);
//float R = analogRead(a)*q;
//Serial.println(R,5);
delay (50);

for (int x=0; x<NDS; x++){ //numero de dados por step
unsigned long t=millis();   
int Vg = analogRead(g);
int Vs = analogRead(s);
int Va = analogRead(a);
int Voffset = analogRead(offset);
int Vads = analogRead(ads);
unsigned long myArray[6] = {t, Vg, Vs, Va, Voffset, Vads};
  
  for (int i = 0; i <= 5; i = i+1) {
 Serial.print(myArray[i]);
 Serial.print(";");
  }
Serial.println("/n");
delay(60);
}
}
}
Serial.println("fim");
delay(10);
exit(0);
}
