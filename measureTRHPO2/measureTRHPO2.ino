/* 
  This sketch measures the temperature, relative humidity, barometric pressure and oxygen level.
  To enable/disable a sensor, uncomment/comment its name in the definitions section below.
*/

//******************************************
//definitions
#define SHT35 //t, rh, dp
#define BME280 //p 

#define INTERVAL (10000)//ms

//******************************************
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_SHT31.h"
#include <Adafruit_BME280.h>

//******************************************
//SHT35
//SHT31 and SHT35 share the same libraries
#ifdef SHT35
Adafruit_SHT31 sht = Adafruit_SHT31();//I2C
#endif

//BME280
#ifdef BME280
Adafruit_BME280 bme;//I2C
#endif

//******************************************
void setup() {
  //Bean Serial is at a fixed baud rate. Changing the value in Serial.begin() has no effect.
  Serial.begin();
  Serial.println("measure TRHPO2");
  Serial.println("v. 0.2");
  #ifdef SHT35
  Serial.print("T[C] RH[%] DP[C] ");
  #endif //SHT35
  #ifdef BME280
  Serial.print("P[hPa] ");
  #endif //BME280
  Serial.print("V[V] ");
  Serial.println();

  //initialize SHT35
  //set to 0x45 for alternate i2c address
  #ifdef SHT35
  sht.begin(0x44);
  #endif

  //initialize BME280
  #ifdef BME280
  bme.begin();
  #endif
  
  //enable wake upon connection
  Bean.enableWakeOnConnect(true);
}

//******************************************
//get dew point
float getDewPoint(float t, float rh){
  if (! isnan(t) and ! isnan(rh)) {
    float h = (log10(rh)-2)/0.4343 + (17.62*t)/(243.12+t);
    return 243.12*h/(17.62-h);
  }
  else return sqrt(-1.);//NaN
}

//******************************************
void loop() {

  //------------------------------------------
  //wake upon connection
  if (Bean.getConnectionState()) {

    //------------------------------------------
    //SHT35
    #ifdef SHT35
    
    //------------------------------------------
    //SHT35 temperature [C]
    float tsht = sht.readTemperature();
    Serial.print(tsht);
    Serial.print(" ");
    
    //------------------------------------------
    //SHT35 humidity [%]
    float rhsht = sht.readHumidity();
    Serial.print(rhsht);
    Serial.print(" ");
    
    //------------------------------------------
    //SHT35 dew point [C]
    Serial.print(getDewPoint(tsht, rhsht));
    Serial.print(" ");

    #endif //SHT35
    //------------------------------------------

    //------------------------------------------
    //BME280
    #ifdef BME280
    
    //------------------------------------------
    //BME280 pressure [hPa]
    Serial.print(bme.readPressure() / 100.);
    Serial.print(" ");

    #endif //BME280
    //------------------------------------------
    
    //------------------------------------------
    //bean temperature [C] (-40 C to 87 C range)
    //Serial.print(Bean.getTemperature());
    //Serial.print(" ");
    
    //------------------------------------------
    //bean voltage [V] (0.01 V/unit)
    Serial.print(Bean.getBatteryVoltage()*0.01);
    Serial.print(" ");
    
    //------------------------------------------

    //new line
    Serial.println();
    
    //sleep
    Bean.sleep(INTERVAL);

  } else {
    
    //sleep until next connection
    Bean.sleep(0xFFFFFFFF);
  }
}
