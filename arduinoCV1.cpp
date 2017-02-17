_____________________HERE IS THE CODE_________________________
++++++++++++++++++++++++++++++++++++++++++++++++++
**************  This is the C++ Arduino storageCode.ino   **********************

//START CODE
//Author: Robert Morris

#include <Servo.h> //import arduino serial library

Servo table; // servo class table initialization
Servo door; // servo class door initialization
int detector; // analog detector variable
String order = ""; // command string variable setup
String inputString = "";         // a string builder for serial communication
boolean stringComplete = false;  // boolean for bytes to  string is completion
unsigned long previousMillis = 0; // long variable for timeout timer
unsigned long currentMillis = 0; // long variable for timeout timer
long interval = 14000; // total time before timeout during analog hand detection

void setup() { // setup for variables and system
  Serial.begin(9600); //master/slave serial channel set
  pinMode(A5, INPUT); //analog light reader pin set
  pinMode(2, OUTPUT); //led for analog reader pin set
  inputString.reserve(200); //reserver buffer size for serial string reader
  door.attach(6);// door motor power attatchment
  door.write(10); // setting door to close position on startup
  //Serial.print("Running");
  delay(1000);
  door.detach();// door motor power detatchment
}

void loop() { // system main loop


    serialEvent(); // checking buffer for serial info from master
   
    if (stringComplete) { // boolean from serial buffer check function
      stringComplete = false; // boolean reset
      order = inputString; // string comparrison setter
     
      //  ---- BEGIN TABLE CONTROL ----
     
      if(order == "turnL"){ //command turn table left
        table.attach(9);// table motor power attactment
        table.write(180);
        delay(1100);
        table.detach(); // table motor power detatchment
      }
     
      else if(order == "turnR"){ //command turn table right
        table.attach(9);// table motor power attactment
        table.write(0);
        delay(1100);
        table.detach();// table motor power detatchment
      }
     
      else if(order == "rotate"){//slow table rotate for calibration
        table.attach(9); // table motor power attactment
        while(stringComplete != true){ //stops with new serial string detected
           table.write(89);
           serialEvent(); // checking for serial string in buffer
        }
        table.detach();// table motor power detatchment
      }
     
//  ---- END TANBLE CONTROL ----

//  ============================     

//  ---- BEGIN DOOR CONTROL ----

      else if(order == "close"){ //command to close door
        //Serial.println("close recieved");
        door.attach(6); // door motor power attatchment
        door.write(10);
        delay(2000);
        door.detach();// door motor power detatchment
      }
     
      else if(order == "open"){ // command to open door, free from detection
        door.attach(6); // door motor power attatchment
        //Serial.print("open recieved");
        door.write(120);
        delay(2000);
        door.detach(); // door motor power detatchment
      }
      else if(order == "openwait"){ // command to open door, wait for hand detection or new string
       digitalWrite(2, HIGH); // led light power for detector
       door.attach(6); // door motor power attatchment
       door.write(120);
       delay(2000);
       detector = analogRead(A5); // analog light reading
       //Serial.println(detector);
       previousMillis = millis(); // timer for timeout on hand detection
       while(detector != 0){ // detectoin loop terminator
         currentMillis = millis(); // timer update
         detector = analogRead(A5); // detector update
         detector -+ 20; // adjustment for over lighting
         if(currentMillis - previousMillis > interval){ // timelapse comparrison
           Serial.println("0"); // serial timeout notification
           break; // timeout loop terminator
         }
       }
       digitalWrite(2, LOW); // turn off light for detector
       Serial.println("1"); // serial detection notification
       door.detach(); // door motor power detatchment
      }
  
//  ---- END DOOR CONTROL ----
  
      inputString = ""; // reset string builder to empty
      order = ""; // reset command string to empty
    }
   }
     

void serialEvent() { // slave serial listener function, waiting for bytes
 
  while (Serial.available()) { // if bytes in buffer
    // get the new byte:
    char inChar = (char)Serial.read(); // typecast bytes from ascii to char
    // add it to the inputString:
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') { // if char new line char
      stringComplete = true; // change boolean true
      break; // break out of reader loop
    }
    inputString += inChar; // adding char to string builder variable
  }
}

//END CODE
