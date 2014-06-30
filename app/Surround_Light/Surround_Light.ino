#include <SoftwareSerial.h>
SoftwareSerial xbee =  SoftwareSerial(2, 3); // RX, TX

static const uint8_t magic[] = {'L','i','v'};
#define MAGIC_SIZE  sizeof(magic)
#define HEADER_SIZE (MAGICS_SIZE + 1)

#define MODE_HEADER 0
#define MODE_HOLD   1
#define MODE_DATA   2

#define SURROUND_INDEX "A"

void setup() {
  uint8_t
    buffer[256],
    indexIn       = 0,
    indexOut      = 0,
    mode          = MODE_HEADER,
    surround_count;
  
  int16_t
    bytesBuffered = 0,
//    hold          = 0,
    c;

  int32_t
    bytesRemaining;

  unsigned long
    startTime,
    lastByteTime,
    lastAckTime,
    t;
  
  startTime    = micros();
  lastByteTime = lastAckTime = millis();
  
  Serial.begin(9600);
  Serial.println("Ready to recieve");
  
  xbee.begin(9600);
  xbee.println("Ready");
  
  for(;;) {
    t = millis();
    
    // cache data each cycle
    if((bytesBuffered < 256) && ((c = xbee.read()) >= 0)) {
      buffer[indexIn++] = c;
      bytesBuffered++;
      lastByteTime = lastAckTime = t;
      
    // No data?
    } else {
      // Check for timeout
      if((t - lastByteTime) > serialTimeout) {
        Serial.println("TODO: Timeout... fade out");
      }
    }
    
    // State Machine
    switch(mode) {
      case MODE_HEADER:
        // is there enough data for us to verify the header?
        if (bytesBuffered >= HEADER_SIZE) {
          // then check for the magicword
          for(i=0; (i<MAGIC_SIZE) && (buffer[indexOut++] == magic[i++]););
          if (i == MAGIC_SIZE) {
            surround_count = buffer[indexOut++];
            bytesRemaining = surround_count * 4L; // Surround Index, R, G & B
            bytesBuffered  = -1;
            mode           = MODE_HOLD;
          }
          bytesBuffered -= i;
        }
        break;
      
      case MODE_HOLD:
        // hold here for a bit - let data steam in
        // XXX: I have a feeling this might be holding a little too long
        if((micros() - startTime) < bytesRemaining) break;
        break;
      
      case MODE_DATA:
    }
    
  }
}

//// loop
//void loop() {
//  // if there's any serial available, read it:
//  while (xbee.available() > 0) {
////    Serial.println(xbee.read());
////    // look for the next valid integer in the incoming serial stream:
////    valueR = xbee.parseInt();
////    valueG = xbee.parseInt();
////    valueB = xbee.parseInt();
////
//    if (xbee.read() == surround_index) {
//      Serial.println("START");
//
//      valueR = xbee.parseInt();
//      valueG = xbee.parseInt();
//      valueB = xbee.parseInt();
//      
//      // look for the end character
//      if (xbee.read() == surround_ender) {
//        Serial.println("END");
////        // set the LEDs
////        setLED(valueR, valueG, valueB);
////      
////        // reset the timeout manager
////        timeout_last_reset = millis();
//      }
//    }
//  }
//  
//  // manage timeouts
////  faded_out = (valueR + valueG + valueB) = 0;
////  if (((timeout_last_reset + timeout_period) < millis()) && !faded_out) {
////    if (logging) {
////      Serial.println("We've reached the timeout");
////    }
////    
////    // fade out & constrain
////    valueR = constrain(valueR-1, 0, 255);
////    valueG = constrain(valueG-1, 0, 255);
////    valueB = constrain(valueB-1, 0, 255);
////    
////    // set the LEDs
////    setLED(valueR, valueG, valueB);
////    
////    // slow down the fade
////    delay(10);
////  }
//}
//
//// test pattern
//void testPattern() {
//  setLED(255,0,0);
//  delay(500);
//  setLED(0,255,0);
//  delay(500);
//  setLED(0,0,255);
//  delay(500);
//  setLED(0,0,0);
//}
//
//// set the LED colours
//void setLED(int r, int g, int b) {
//  // My LEDs are common-cathode, so big number = low energy
//  analogWrite(ledR, map(r, 0, 255, 255, 0));
//  analogWrite(ledG, map(g, 0, 255, 255, 0));
//  analogWrite(ledB, map(b, 0, 255, 255, 0));
//  
//  // output the current versions
//  if (logging) {
//    Serial.print(valueR);
//    Serial.print(" - ");
//    Serial.print(valueG);
//    Serial.print(" - ");
//    Serial.println(valueB);
//  }
//}
