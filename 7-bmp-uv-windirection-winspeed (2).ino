#include <SFE_BMP180.h>
#include <Wire.h>

SFE_BMP180 pressure;

#define ALTITUDE 90.0 

int UV_OUT = A0;    
int REF_3V3 = A1;   


void setup()
{
  Serial.begin(9600);

  if (pressure.begin()) {
  }
  else
  {
    while(1);
  }
}

void loop()
{
  float sensorValue1 = analogRead(A3);
  float voltage1 = (sensorValue1 / 1024) * 5;
  float wind_speed = mapfloat(voltage1, 0.4, 2, 0, 32.4);
  float speed_mph = ((wind_speed *3600)/1609.344);
  int sensorValue = analogRead(A2);
  float voltage = sensorValue*5/1023.0;
  int direction = map(sensorValue, 0, 1023, 0, 360);
  int uv_Level = analogRead_average(UV_OUT);
  int ref_Level = analogRead_average(REF_3V3);
  float output_Voltage = 3.3 / ref_Level * uv_Level;

  float uvIntensity = mapfloat(output_Voltage, 0.99, 2.8, 0.0, 15.0);	
  char status;
  double T,P,p0,a;
  status = pressure.startTemperature();
  if (status != 0)
  {
    delay(status);
    status = pressure.getTemperature(T);
    if (status != 0)
    {
      status = pressure.startPressure(3);
      if (status != 0)
      {
        delay(status);
        status = pressure.getPressure(P,T);
        if (status != 0)
        {
          p0 = pressure.sealevel(P,ALTITUDE);
          a = pressure.altitude(P,p0);

          Serial.print("wind_speed_analog_value:");
          Serial.print(sensorValue1);
          Serial.print(",wind_speed_voltage:");
          Serial.print(voltage1);
          Serial.print(" V,wind_speed(m/s):");
          Serial.print(wind_speed);
          Serial.print(" m/s,wind_speed(mph):");
          Serial.print(speed_mph);
          Serial.print(" mph,wind_direction_ADC:");
          Serial.print(sensorValue);
          Serial.print(",wind_direction_voltage:");
          Serial.print(voltage);
          Serial.print(" V,wind_direction_direction:");
          Serial.print(direction);
          Serial.print(",ML8511_output:");
          Serial.print(uv_Level);
          Serial.print(",ML8511_voltage:");
          Serial.print(output_Voltage);
          Serial.print(" V,UV_Intensity(mW/cm^2):");
          Serial.print(uvIntensity);
          Serial.print(" mW/cm^2,BMP180_provided_altitude(meters):");
          Serial.print(ALTITUDE, 0);
          Serial.print(" meters,BMP180_provided_altitude(feet):");
          Serial.print(ALTITUDE*3.28084, 0);
          Serial.print(" feet,BMP180_temperature(*C):");
          Serial.print(T, 2);
          Serial.print(" *C,BMP180_temperature(*F):");
          Serial.print((9.0/5.0)*T+32.0,2);
          Serial.print(" *F,BMP180_absolute_pressure(mb):");
          Serial.print(P, 2);
          Serial.print(" mb,BMP180_absolute_pressure(inHg):");
          Serial.print(P*0.0295333727, 2);
          Serial.print(" inHg,BMP180_relative(sea-level)pressure(mb):");
          Serial.print(p0,2);
          Serial.print(" mb,BMP180_relative(sea-level)pressure(inHg):");
          Serial.print(p0*0.0295333727,2);
          Serial.print(" inHg,BMP180_computed_altitude(meters):");
          Serial.print(a, 0);
          Serial.print(" meters,BMP180_computed_altitude(feet):");
          Serial.print(a*3.28084, 0);
          Serial.println(" feet");
        }
      }
    }
  }
  
  delay(5000);
} 


int analogRead_average(int pinToRead)
{
  int NumberOfSamples = 8;
  int runningValue = 0; 

  for(int x = 0; x < NumberOfSamples; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= NumberOfSamples;

  return(runningValue);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
