#include <WiFiS3.h>       // For Arduino Uno R4 WiFi
#include <ThingSpeak.h>   // Always include after WiFi libraries

char ssid[] = "Stevens-IoT";     // your network SSID
char pass[] = "pVt469TQZ7";      // your network password

WiFiClient client;

unsigned long myChannelNumber = 2877004;
const char * myWriteAPIKey = "3VI96UKBSDR2T4BC";

int number = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for native USB connection
  }

  WiFi.begin(ssid, pass);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("\nConnected to WiFi.");
  ThingSpeak.begin(client);
}

void loop() {
  int x = ThingSpeak.writeField(myChannelNumber, 1, number, myWriteAPIKey);

  if (x == 200) {
    Serial.println("Channel update successful.");
  } else {
    Serial.print("Problem updating channel. HTTP error code ");
    Serial.println(x);
  }

  number = (number + 1) % 100;
  delay(20000);
}
