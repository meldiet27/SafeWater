#include <WiFiS3.h>
#include <ThingSpeak.h>

char ssid[] = "Stevens-IoT";
char pass[] = "pVt469TQZ7";

WiFiClient client;

unsigned long myChannelNumber = 2877004;
const char * myWriteAPIKey = "3VI96UKBSDR2T4BC";
const char * myReadAPIKey = "00YSVLHONG1542DI";

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
  // Read command from field2
  String command = ThingSpeak.readStringField(myChannelNumber, 2, myReadAPIKey);

  if (command == "START") {
    Serial.println("Received START command. Measuring...");

    int x = ThingSpeak.writeField(myChannelNumber, 1, number, myWriteAPIKey);
    if (x == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.print("Problem updating channel. HTTP error code ");
      Serial.println(x);
    }

    number = (number + 1) % 100;

    // Clear command after execution
    ThingSpeak.writeField(myChannelNumber, 2, "", myWriteAPIKey);
  }

  delay(5000); // Wait before checking command again
}
