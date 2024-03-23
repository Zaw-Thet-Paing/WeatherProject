import Adafruit_DHT.__init__
import serial
from datetime import datetime
import time
from gpiozero import Buzzer, InputDevice
import random
import pymongo
import sys
import pyfiglet

connection = pymongo.MongoClient("mongodb+srv://DBuser1:7NPAlVviHjPvzY42@cluster007.4tiahbt.mongodb.net/?retryWrites=true&w=majority")
database = connection["sensor_table"]

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

buzz = Buzzer(13)
no_rain = InputDevice(18)
cur_time = datetime.now()
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=5)

def buzz_now(iter):
    for i in range(iter):
        buzz.on()
        time.sleep(0.1)
        buzz.off()
        time.sleep(0.1)

def read_arduino_data():
    arduino.write(bytes("request", 'utf-8'))
    data = arduino.readline()
    data = str(data)[2:-5]
    if "wind_speed_analog_value" in data:
        return data
    else:
        return None

result = pyfiglet.figlet_format("IoT Project") 
print(result)
print()

while True:
    try:
        arduino_response_data = read_arduino_data()
        
        if arduino_response_data:        
            cur_date = datetime.now().date()
            collection_name_copy = cur_date.strftime("%Y-%m-%d")
            collection = database[collection_name_copy]
            
            Data = {}
            Data["Day"] = datetime.now().strftime("%Y-%m-%d")
            Data["Time"] = datetime.now().strftime("%H:%M")
            
            hud, tem = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            Data["DHT22_temperature"] = tem
            Data["DHT22_humidity"] = hud

            if not no_rain.is_active:
                Data["RainDrop"] = "It's raining"
                buzz_now(2)
            else:
                Data["RainDrop"] = "No rain"
            
            for i in arduino_response_data.split(","):
                key, value = i.split(":")
                Data[key] = value
            collection.insert_one(Data)
            print("\033[32mPrinting data from sensors...\033[0m")
            print("\033[32m#############################\033[0m\n")
            print("\033[93mDHT22 Temperature\033[0m : \033[31m{:.2f}*C\033[0m".format(tem))
            print("\033[93mDHT22 Humidity\033[0m    : \033[31m{:.2f}%\033[0m".format(hud))
            print()
            print("\033[93mDHT22 Raindrop status\033[0m : \033[31m{}\033[0m".format(Data['RainDrop']))
            print()
            print("\033[93mWind Speed Analog Value\033[0m : \033[31m{}\033[0m".format(Data['wind_speed_analog_value']))
            print("\033[93mWind Speed Voltage\033[0m      : \033[31m{}\033[0m".format(Data['wind_speed_voltage']))
            print("\033[93mWind Speed (m/s)\033[0m        : \033[31m{}\033[0m".format(Data['wind_speed(m/s)']))
            print("\033[93mWind Speed (mph)\033[0m        : \033[31m{}\033[0m".format(Data['wind_speed(mph)']))
            print()
            print("\033[93mWind direction\033[0m : \033[31m{} degree\033[0m".format(Data['wind_direction_direction']))
            print()
            print("\033[93mUltraviolet output\033[0m             : \033[31m{}\033[0m".format(Data['ML8511_output']))
            print("\033[93mUltraviolet Voltage\033[0m            : \033[31m{}\033[0m".format(Data['ML8511_voltage']))
            print("\033[93mUltraviolet Intensity(mW/cm^2)\033[0m : \033[31m{}\033[0m".format(Data['UV_Intensity(mW/cm^2)']))
            print()
            print("\033[93mBMP180 altitude(meters)\033[0m                  : \033[31m{}\033[0m".format(Data['BMP180_provided_altitude(meters)']))
            print("\033[93mBMP180 altitude(feet)\033[0m                    : \033[31m{}\033[0m".format(Data['BMP180_provided_altitude(feet)']))
            print("\033[93mBMP180 temperature(*C)\033[0m                   : \033[31m{}\033[0m".format(Data['BMP180_temperature(*C)']))
            print("\033[93mBMP180 temperature(*F)\033[0m                   : \033[31m{}\033[0m".format(Data['BMP180_temperature(*F)']))
            print("\033[93mBMP180 absolute pressure(mb)\033[0m             : \033[31m{}\033[0m".format(Data['BMP180_absolute_pressure(mb)']))
            print("\033[93mBMP180 absolute pressure(inHg)\033[0m           : \033[31m{}\033[0m".format(Data['BMP180_absolute_pressure(inHg)']))
            print("\033[93mBMP180 relative sea level pressure(mb)\033[0m   : \033[31m{}\033[0m".format(Data['BMP180_relative(sea-level)pressure(mb)']))
            print("\033[93mBMP180 relative sea level pressure(inHg)\033[0m : \033[31m{}\033[0m".format(Data['BMP180_relative(sea-level)pressure(inHg)']))
            print("\033[93mBMP180 computed altitude(meters)\033[0m         : \033[31m{}\033[0m".format(Data['BMP180_computed_altitude(meters)']))
            print("\033[93mBMP180 computed altitude(feet)\033[0m           : \033[31m{}\033[0m".format(Data['BMP180_computed_altitude(feet)']))
            
            print("\n")
        else:
            continue
    except KeyboardInterrupt:
        print("Closed....")
        sys.exit()
        
