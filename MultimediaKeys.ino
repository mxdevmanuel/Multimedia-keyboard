#include <Pushbutton.h>

#define LED_PIN 13

Pushbutton volumeDown(12);
Pushbutton mute(11);
Pushbutton volumeUp(10);
Pushbutton play(9);
Pushbutton next(7);
Pushbutton prev(8);
  
void setup()
{
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  handshake();
}

void loop()
{
  while (1)
  {
    if (volumeDown.getSingleDebouncedRelease())
    {
      Serial.write(0x42);
    }

    if(mute.getSingleDebouncedRelease())
    {
      Serial.write(0x41);
    }

    if(volumeUp.getSingleDebouncedRelease())
    {
      Serial.write(0x43);
    }

    if(play.getSingleDebouncedRelease())
    {
      Serial.write(0x44);
    }
    
    if(next.getSingleDebouncedRelease())
    {
      Serial.write(0x45);
    }
    
    if(prev.getSingleDebouncedRelease())
    {
      Serial.write(0x46);
    }
    
    }
 }

 void handshake()
 {
      while(Serial.available() <= 0)
      {
        Serial.write('Z');
        delay(200);
      }
 }
 

