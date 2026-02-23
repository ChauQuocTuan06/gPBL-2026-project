#define PIR_PIN 8
#define BUZZER_PIN 9
unsigned long previous_time=0;
unsigned long next_time=500;
void setup(){
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.print("start pir, wait 30 seconds");
  delay(5000);
}

void loop(){
  unsigned long current_time = millis();
  int motion = digitalRead(PIR_PIN);
  if(motion == HIGH){
    digitalWrite(BUZZER_PIN, LOW);
    Serial.println("Konichiwa!");
  }
  else
  {
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("Nothing");
  }
  delay(100);
}