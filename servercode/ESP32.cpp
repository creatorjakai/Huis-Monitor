#include <WiFi.h>

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
  
  Serial.println("\nVerbonden met WiFi");
  Serial.print("IP Adres: ");
  Serial.println(WiFi.localIP());
  
  server.begin();
  Serial.println("not: SERVER GESTART");
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("not: Nieuwe client verbonden. Wachten op wachtwoord...");
    
    String inputPassword = "";
    bool authenticated = false;

    // Lees het wachtwoord dat de client stuurt (tot aan een nieuwe regel)
    unsigned long startTime = millis();
    while (client.connected()) {
      if (client.available()) {
        inputPassword = client.readStringUntil('\n');
        inputPassword.trim(); // Verwijder spaties en lege plekken
        break;
      }
      //Zet hier hoelang je tijd hebt om het wachtwoord in te typen
      if (millis() - startTime > 5000) {
        Serial.println("not: Time-out: geen wachtwoord ontvangen.");
        client.stop();
        return;
      }
    }

    // Controleer het wachtwoord
    if (inputPassword == SERVER_PASSWORD) {
      authenticated = true;
      Serial.println("not: Wachtwoord correct! Toegang verleend.");
      client.println("LOGIN_OK"); // Stuur bevestiging naar de Computer
    } else {
      Serial.println("not: Fout wachtwoord! Verbinding verbroken.");
      client.println("LOGIN_FAILED");
      delay(100);
      client.stop(); // Verbreek de verbinding met de Computer
      return;
    }

    //Hier moet je het script zetten voor data uitwisseling
    //Dit is voor data ontvangen
    if (authenticated) {
      while (client.connected()) {
        if (client.available()) {
          String data = client.readStringUntil('\n');
          Serial.println(data);
          
          //Hier moet je iets zetten als je iets terug naar de Computer wil sturen
          client.println("ESP32 zegt: Hallo!");
        }
      }
      client.stop();
    }
  }
}   
