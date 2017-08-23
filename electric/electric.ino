#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define WLAN_SSID       "ssid"
#define WLAN_PASS       "wifi pwd"
#define FEED_PATH "carlosyLeo/"
//define leds GPIO
int WIFI_LED    =  15  ;
int MQTT_LED    =  14  ;
int RED_LED     =  16  ;
int YELLOW_LED  =  5   ;
int GREEN_LED   =  4   ;

WiFiClient espClient;
//const char* mqtt_server   = "iot.eclipse.org"; //mqtt connection is unstable to this free server!!!

const char* mqtt_server   = "use your private mqtt server";
#define USERNAME  "mqtt user"
#define PASSWORD  "mqtt pwd"

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  //Var for store message
  String msg ="";
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    msg = msg+(char)payload[i];
  }
  Serial.println(msg);
  //switch off leds
  digitalWrite(RED_LED,LOW);
  digitalWrite(YELLOW_LED,LOW);
  digitalWrite(GREEN_LED,LOW);
  //switch on only the led matching to mqtt message
  if(msg=="red"){
    digitalWrite(RED_LED,HIGH);
  } else if(msg=="yellow"){
    digitalWrite(YELLOW_LED,HIGH);
  }else if(msg=="GREEN"){
    digitalWrite(GREEN_LED,HIGH);
  }
  Serial.println();
}

PubSubClient client(espClient);

//Connect to wifi network
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  digitalWrite(WIFI_LED,LOW);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(WIFI_LED,HIGH);
    delay(500);
    Serial.print(".");
    digitalWrite(WIFI_LED,LOW);
    delay(500);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  digitalWrite(WIFI_LED,HIGH);
}

//connect/reconnect to mqtt server
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    digitalWrite(MQTT_LED,LOW);
    // Attempt to connect
    if (client.connect("arduinoClient", USERNAME, PASSWORD)) {
      digitalWrite(MQTT_LED,HIGH);
      Serial.println("connected");
      client.subscribe("carlosyLeo/");
    } else {
      digitalWrite(MQTT_LED,LOW);
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying and flash mqtt led
      digitalWrite(MQTT_LED,HIGH);
      delay(500);
      digitalWrite(MQTT_LED,LOW);
      delay(500);
      digitalWrite(MQTT_LED,HIGH);
      delay(500);
      digitalWrite(MQTT_LED,LOW);
      delay(3500);
    }
  }
}

void setup() {  
  Serial.begin(9600);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  //setup leds
  pinMode(WIFI_LED,OUTPUT);
  pinMode(MQTT_LED,OUTPUT);
  pinMode(RED_LED,OUTPUT);
  pinMode(YELLOW_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  //switch off all leds
  digitalWrite(WIFI_LED,LOW);
  digitalWrite(MQTT_LED,LOW);
  digitalWrite(RED_LED,LOW);
  digitalWrite(YELLOW_LED,LOW);
  digitalWrite(GREEN_LED,LOW);
  setup_wifi();
  delay(1500);
}

void loop() {
  if(WiFi.status()==WL_CONNECTED){
    if (!client.connected()) {
      Serial.println("reconnect()");
      reconnect();
    }
    client.loop();
  }
  delay(500);
}
