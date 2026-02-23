#define VIB_PIN 8
#define BUZZER_PIN 12
#define TOUCH_PIN 10
int knockCount = 0;
unsigned long firstKnockTime = 0;
unsigned long knockWindow = 2000;  
unsigned long debounceTime = 200;   
unsigned long lastKnock = 0;
unsigned long lastTouch = 0;
bool touchs = false;
void setup() {
  pinMode(VIB_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(TOUCH_PIN, INPUT);
  Serial.begin(9600);
}

void loop() {
  int vibration = digitalRead(VIB_PIN);
  int touch = digitalRead(TOUCH_PIN);
  unsigned long currentTime = millis();
  if(touch == HIGH){
    lastTouch = currentTime;
    touchs = true;
  }
  if(touchs == true) {
    Serial.println("helloooooooooooooooooooooooooooooooooooooooooooooooooo");
    if (vibration == HIGH && (currentTime - lastKnock > debounceTime)) {
      
      lastKnock = currentTime;

      if (knockCount == 0) {
        firstKnockTime = currentTime; 
      }

      knockCount++;
      Serial.print("Knock: ");
      Serial.println(knockCount);
    }
    if (knockCount == 3 && (currentTime - firstKnockTime <= knockWindow)) {
      Serial.println("3 knocks detected!");
      digitalWrite(BUZZER_PIN, LOW);
      delay(5000);
      digitalWrite(BUZZER_PIN, HIGH);
      knockCount = 0;
    }
    if (currentTime - firstKnockTime > knockWindow) {
      knockCount = 0;
    }
  }
  else{
    Serial.println("Nothing");
    digitalWrite(BUZZER_PIN, HIGH);
  }
  delay(300);
}