#include <ESP8266WiFi.h>

const char* ssid = "JOUW_SSID";
const char* password = "JOUW_WACHTWOORD";
const char* SERVER_PASSWORD = "11223344";

WiFiServer server(5000);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Verbonden met WiFi");
  Serial.print("IP Adres: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("SERVER GESTART");
}

void loop() {

  WiFiClient client = server.available();

  if (!client)
    return;

  Serial.println("Nieuwe client verbonden.");

  String inputPassword;

  unsigned long start = millis();

  while (client.connected()) {

    if (client.available()) {
      inputPassword = client.readStringUntil('\n');
      inputPassword.trim();
      break;
    }

    if (millis() - start > 5000) {
      client.stop();
      return;
    }
  }

  if (inputPassword != SERVER_PASSWORD) {
    client.println("LOGIN_FAILED");
    client.stop();
    return;
  }

  client.println("LOGIN_OK");

  while (client.connected()) {

    if (client.available()) {

      String data = client.readStringUntil('\n');

      Serial.println(data);

      client.println("ESP8266 zegt: Hallo!");
    }
  }

  client.stop();
}
