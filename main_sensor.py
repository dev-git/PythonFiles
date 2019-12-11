# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author:
# Comments:
# Measures temperature (DS18B20), carbon monoxide (MQ7)=orange, air quality (MQ135)=blue and
# outputs to LCD
# https://components101.com/sensors/mq135-gas-sensor-for-air-quality

import os
import glob
import time
import datetime
import boto3
import pickle
from time import gmtime, strftime
from RPLCD.gpio import CharLCD
from RPi import GPIO

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# DynamoDb
AWS_ACCESS_KEY = 
AWS_SECRET_ACCESS = 
TABLE_NAME = 'sensordata'

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Set up LCD
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '22*')[0]
device_file = device_folder + '/w1_slave'
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 15], numbering_mode=GPIO.BOARD)
#lcd.autoscroll(true)
#lcd = CharLCD()
lcd.write_string(u'Hello world!!')

# Temperature functions
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c#, temp_f

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('Time      | Orange |  Blue |'.format(*range(8)))
print('-' * 18 )

# Create log file
f = open('log.txt', 'w')
f.write('Time     | Orange |  Blue |\n')
f.write('-' * 18)
f.write('\n')

client = boto3.client('dynamodb',  aws_access_key_id=AWS_ACCESS_KEY,  aws_secret_access_key=AWS_SECRET_ACCESS, region_name='ap-southeast-2')

# Main program loop.
while True:
    # Read the temp
    temp = read_temp()
    print(temp)	
    # Read all the ADC channel values in a list.
    values = [0]*2
    for i in range(2):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)


    # Print the ADC values.
    #print(strftime('%H:%M:%S ', gmtime()))

    outStr = 'C, CO-{0}ppm, AQ-{1}ppm'.format(*values)     
    print(outStr)	
    #print('| {0:>6} | {1:>4}  |'.format(*values))

    # Print to the LCD	
    lcd.clear()
    lcd.write_string(str(temp) + outStr)

    # Write to the log file
    #f.write(strftime('%H:%M:%S', gmtime()))
    #f.write('| {0:>6} | {1:>4}  |\n'.format(*values))

    # Write to DynamoDB
    when = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    # temperature
    response = client.put_item(TableName=TABLE_NAME, Item = {'sensorid': {'N':'1'}, 'reading': {'N':str(temp)}, 'whenread': {'S':when}})
    # MQ7 - Carbon monoxide
    response = client.put_item(TableName=TABLE_NAME, Item = {'sensorid': {'N':'2'}, 'reading': {'N':str(values[0])}, 'whenread': {'S':when}})
    # MQ135 - Air quality
    response = client.put_item(TableName=TABLE_NAME, Item = {'sensorid': {'N':'3'}, 'reading': {'N':str(values[1])}, 'whenread': {'S':when}})

    # Pause for half a second.
    time.sleep(30)

print('Closing file...')
f.close()
lcd.close(clear=True)
