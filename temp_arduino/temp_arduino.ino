#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

String condition = "";
int count = 1;
unsigned long lastTime = 0;
const unsigned long interval = 5000; // 5 seconds

void setup() {
  Serial.begin(9600);
  Wire.begin();

  delay(2000);  // Wait for serial and sensor

  if (!mlx.begin()) {
    Serial.println("❌ Failed to connect to MLX90614 sensor!");
    while (1);
  }

  Serial.println("📍 Please enter the condition :");

  // Wait for user to input condition via Serial
  while (condition.length() == 0) {
    if (Serial.available()) {
      condition = Serial.readStringUntil('\n');
      condition.trim();
      if (condition.length() == 0) {
        Serial.println("❗ Empty input. Enter condition again:");
      }
    }
  }

  Serial.print("✅ Condition set to: ");
  Serial.println(condition);
  Serial.println("S.No, Timestamp, Temperature (°C), Condition");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;

    float temperature = mlx.readAmbientTempC();

    // Get current time in "HH:MM:SS" format
    unsigned long sec = millis() / 1000;
    int hours = (sec / 3600) % 24;
    int minutes = (sec / 60) % 60;
    int seconds = sec % 60;

    char timestamp[9];
    sprintf(timestamp, "%02d:%02d:%02d", hours, minutes, seconds);

    // Output format: s.no, timestamp, temperature, condition
    Serial.print(count);
    Serial.print(", ");
    Serial.print(timestamp);
    Serial.print(", ");
    Serial.print(temperature, 2);
    Serial.print(", ");
    Serial.println(condition);

    count++;
  }
}
