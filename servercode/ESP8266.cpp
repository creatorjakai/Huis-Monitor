#include <ESP8266WiFi.h>

//Hier zet je de naam van jouw netwerk
const char* ssid = "JOUW_SSID";
//Hier het wachtwoord van jouw netwerk
const char* password = "JOUW_WACHTWOORD";
//Als je je wachtwoord van de server wil veranderen moet dat hier
const char* SERVER_PASSWORD = "11223344";

//Hier zet je de port waar je je server op host
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
    // Lees het wachtwoord dat de client stuurt (tot aan een nieuwe regel)
    if (client.available()) {
      inputPassword = client.readStringUntil('\n');
      // Verwijder spaties en lege plekken
      inputPassword.trim();
      break;
    }
    //Zet hier hoelang je tijd hebt om het wachtwoord in te typen
    if (millis() - start > 5000) {
      client.stop();
      return;
    }
  }
  // Controleer het wachtwoord
  if (inputPassword != SERVER_PASSWORD) {
    client.println("LOGIN_FAILED");
    client.stop(); // Verbreek de verbinding met de Computer
    return;
  }
  // Stuur bevestiging naar de Computer
  client.println("LOGIN_OK");
  //Hier moet je het script zetten voor data uitwisseling
  while (client.connected()) {
    if (client.available()) {
      //Dit is voor data ontvangen
      String data = client.readStringUntil('\n');
      Serial.println(data);
      //Hier moet je iets zetten als je iets terug naar de Computer wil sturen
      client.println("ESP8266 zegt: Hallo!");
    }
  }
  client.stop();
}
