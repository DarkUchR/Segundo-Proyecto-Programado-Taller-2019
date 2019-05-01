#include <ESP8266WiFi.h>

//Cantidad maxima de clientes es 1
#define MAX_SRV_CLIENTS 1
//Puerto por el que escucha el servidor
#define PORT 7070

/*
 * ssid: Nombre de la Red a la que se va a conectar el Arduino
 * password: Contraseña de la red
 */
const char* ssid = "bryan";
const char* password = "12345678";


// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

/*
 * Intervalo de tiempo que se espera para comprobar que haya un nuevo mensaje
 */
unsigned long previousMillis = 0, temp = 0;
const long interval = 100;

/*
 * Pin donde está conectado el sensor de luz
 * Señal digital, lee 1 si hay luz y 0 si no hay.
 */
#define ldr D8
#define bat A0
/*
 * Variables para manejar las luces con el registro de corrimiento
 */
#define ab  D6
#define clk D7
/*
 * Variables para controlar los motores.
 */
#define EnA D4 // 
#define In1 D3 // D4 en HIGH : retroceder
#define In2 D2 // D3 en HIGH : avanzar
#define In3 D1 // 
#define EnB D5 // 
#define In4 D0// 0 para ir hacia adelante
#define Buzzer 1


/**
 * Variables:
 * data son las luces encedidas/apagadas
 * tiempoCirculo es el tiempo que dura el carro en girar en circulo
 */
byte data = B11111111;
int tiempoCirculo=10000;
/**
 * Función de configuración.
 */
void setup() {
  Serial.begin(115200);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  pinMode(EnA,OUTPUT);
  pinMode(EnB,OUTPUT);
  pinMode(clk,OUTPUT);
  pinMode(ab,OUTPUT);  
  pinMode(ldr,INPUT);

  // ip estática para el servidor
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  // Modo para conectarse a la red
  WiFi.mode(WIFI_STA);
  // Intenta conectar a la red
  WiFi.begin(ssid, password);
  
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("\nCould not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.print("\nConnection Succeeded to: "); Serial.println(ssid);
    Serial.println(".....\nWaiting for a client at");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("Port: ");
    Serial.print(PORT);
  }
  server.begin();
  server.setNoDelay(true);

}

/*
 * Función principal que llama a las otras funciones y recibe los mensajes del cliente
 * Esta función comprueba que haya un nuevo mensaje y llama a la función de procesar
 * para interpretar el mensaje recibido.
 */
void loop() {
  
  unsigned long currentMillis = millis();
  uint8_t i;
  //verifica si hay nuevos clientes
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      //encuentra nuevos espacios libres
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //si no hay espacios libres lo rechaza
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      // El cliente existe y está conectado
      if (serverClients[i] && serverClients[i].connected()) {
        // El cliente tiene un nuevo mensaje
        if(serverClients[i].available()){
          // Leemos el cliente hasta el caracter '\r'
          String mensaje = serverClients[i].readStringUntil('\r');
          // Eliminamos el mensaje leído.
          serverClients[i].flush();
          
          // Preparamos la respuesta para el cliente
          String respuesta; 
          procesar(mensaje, &respuesta);
          Serial.println(mensaje);
          // Escribimos la respuesta al cliente.
          serverClients[i].println(respuesta);
        }  
        serverClients[i].stop();
      }
    }
  }
}

/*
 * Función para dividir los comandos en pares llave, valor
 * para ser interpretados y ejecutados por el Carro
 * 
 */
void procesar(String input, String * output){
  //Buscamos el delimitador ;
  Serial.println("Checking input....... ");
  int comienzo = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',comienzo);
  
  while(delComa>0){
    String comando = input.substring(comienzo, delComa);
    Serial.print("Processing comando: ");
    Serial.println(comando);
    del2puntos = comando.indexOf(':');
    /*
    * Si el comando tiene ':', es decir tiene un valor
    * se llama a la función exe 
    */
    if(del2puntos>0){
        String llave = comando.substring(0,del2puntos);
        String valor = comando.substring(del2puntos+1);

        Serial.print("(llave, valor) = ");
        Serial.print(llave);
        Serial.println(valor);
        //Una vez separado en llave valor 
        *output = implementar(llave,valor); 
    }
    else if(comando == "sense"){
      *output = getSense();         
    }
    else if(comando=="Infinite"){
    /*
    * Se gira en forma de infinito
    */
      mover(0);
      girarDerecha();
      delay(100);
      mover(1000);
      delay(tiempoCirculo/2);
      mover(0);
      girarIzquierda();
      delay(100);
      mover(1000);
      delay(tiempoCirculo);
      mover(0);
      girarDerecha();
      delay(100);
      mover(1000);
      delay(tiempoCirculo/2);
      mover(0);
      noGirar();
    }
    else if(comando=="ZigZag"){
    /*
    * Se avanza en zigzag
    */
      for(int i=0;i<2;i++){
        mover(0);
        girarDerecha();
        delay(100);
        mover(1000);
        delay(tiempoCirculo/4);
        mover(0);
        girarIzquierda();
        delay(100);
        mover(1000);
        delay(tiempoCirculo/4);
      }
      mover(0);
      noGirar();
    }else if(comando=="indeciso"){
    /*
    * Se va hacia adelante y hacia atras repetidamente
    */
      for(int i=1;i<3;i++){
        mover(1023);
        delay(500*i);
        mover(0);
        delay(500);
        mover(-1023);
        delay(500*i);
        mover(0);
        delay(500);
      }        
    }else if(comando=="parpadear"){
    /*
    * Todas las luces parpadean por unos segundos
    */
      for(int i=1;i<10;i++){
        data=00000000;
        shiftOut(ab, clk, LSBFIRST, data); 
        delay(500);
        data=11111111;
        shiftOut(ab, clk, LSBFIRST, data); 
        delay(500);
      }        
    }else if(comando=="girarFacil"){
    /*
    * El carro se da vuelta, girando hacia la derecha, y luego retrocediendo hacia la izquierda
    */
      mover(0);
      girarDerecha();
      delay(100);
      mover(1000);
      delay(tiempoCirculo/2);
      mover(0);
      girarIzquierda();
      delay(100);
      mover(-1000);
      delay(tiempoCirculo/2);
      mover(0);   
    }
    else{
      Serial.print("Comando no reconocido. Solo presenta llave");
      *output = "Undefined key value: " + comando+";";
    }
    comienzo = delComa+1;
    delComa = input.indexOf(';',comienzo);
  }
}

/*
 *  Esta funcion hace que gire a la izquierda
* E: Ninguna
* S: Ninguna
* R: Ninguna
*/
void girarIzquierda(){
  Serial.println("Girando izquierda");
  //# AGREGAR CÓDIGO PARA GIRAR IZQUIERDA
  digitalWrite(In3, HIGH); 
  digitalWrite(In4, LOW); 
  digitalWrite(EnB, HIGH);
}

/*
 * Esta funcion hace que gire a la derecha
* E: Ninguna
* S: Ninguna
* R: Ninguna
*/
void girarDerecha(){
  Serial.println("Girando derecha");
  digitalWrite(In3, LOW); 
  digitalWrite(In4, HIGH); 
  digitalWrite(EnB, HIGH); 
}

/*
* Esta funcion elimina cualquier giro 
* E: Ninguna
* S: Ninguna
* R: Ninguna
*/
void noGirar(){
  Serial.println("directo");
  digitalWrite(EnB, LOW);   
}

/*
* Esta funcion hace que se muevan los motores de desplazamiento
* E: Un entero con el valor de la potencia
* S: Ninguna
* R: Ninguna
*/
void mover(int valor){
  Serial.print("Move....: ");
    Serial.println(valor);
    if (valor >0){
        digitalWrite(In1, HIGH); 
        digitalWrite(In2, LOW); 
    }else{
        digitalWrite(In2, HIGH); 
        digitalWrite(In1, LOW); 
    }
    if(abs(valor)<1023){
      analogWrite(EnA,abs(valor));
    }else{
      analogWrite(EnA,1023);
    }
}

/*
* Esta funcion cambia las luces a como se le indique
* E: LLave, Valor(Un string y un entero)
* S: Ninguna
* R: Niguna
*/
void cambiarLuces(String llave,String valor){
  switch (llave[1]){
      case 'f':
        Serial.println("Luces frontales");
        if(valor=="1"){
          byte frontales = B11111110;
          data=data&frontales;
        }
        else if(valor=="0"){
          byte frontales = B00000001;
          data=data|frontales;
        }
        break;
      case 'b':
        Serial.println("Luces traseras");
        if(valor=="1"){
          byte traseras = B11001111;
          data=data&traseras;
        }
        else if(valor=="0"){
          byte traseras = B00110000;
          data=data|traseras;
        }
        break;
      case 'l':
        Serial.println("Luces izquierda");
        if(valor=="1"){
          byte izquierda = B11011111;
          data=data&izquierda;
        }
        else if(valor=="0"){
          byte izquierda = B00100000;
          data=data|izquierda;
        }
        break;
      case 'r':
        Serial.println("Luces derechas");
        if(valor=="1"){
          byte derecha = B11101111;
          data=data&derecha;
        }
        else if(valor=="0"){
          byte derecha = B00010000;
          data=data|derecha;
        }
        break;
      default:
        Serial.println("Ninguna de las anteriores");
        break;  
    }
    Serial.println(data);
    shiftOut(ab, clk, LSBFIRST, data);
}

String implementar(String llave, String valor){
  String result="ok;";
  Serial.print("Comparing llave: ");
  Serial.println(llave);
  if(llave == "pwm"){
    mover(valor.toInt());
  }
 
  else if(llave == "dir"){
    switch (valor.toInt()){
      case 1:
        girarDerecha();
        break;
      case -1:
        girarIzquierda();
        break;
       default:
        noGirar();
        break;
    }
  }
  else if(llave[0] == 'l'){
    Serial.println("Cambiando Luces");
    Serial.print("valor luz: ");
    Serial.println(valor);
    cambiarLuces(llave,valor);
    
  }
  else if(llave=="Circle"){
   /**
   *Aqui se hace mover en circulo al carro
   */
    if (valor=="1" || valor=="-1"){
      if (valor=="1"){
        girarDerecha();
      }else if(valor=="-1"){
        girarIzquierda();
      }
      bocina(1000,500);
      delay(100);
      mover(1000);
      delay(20000);
      mover(0);
      noGirar();
    }  
    else{
      result = "Undefined key value: " + llave+";";
      Serial.println(result);
    }
  }
  /**
   * El comando tiene el formato correcto pero no tiene sentido para el servidor
   */
  else{
    result = "Undefined key value: " + llave+";";
    Serial.println(result);
  }
  return result;
}

/**
 * Función para obtener los valores de telemetría del auto
 */
String getSense(){
  int batteryLvl = 100*analogRead(bat)/1023;
  int light = digitalRead(ldr);

  // EQUIVALENTE A UTILIZAR STR.FORMAT EN PYTHON, %d -> valor decimal
  char sense [16];
  sprintf(sense, "blvl:%d;ldr:%d;", batteryLvl, light);
  return sense;
}
