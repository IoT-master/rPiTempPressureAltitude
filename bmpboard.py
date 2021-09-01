#/home/pi/environ/.venv/bin/python3
import time
import board
import json
from pushbullet import Pushbullet
# import digitalio # For use with SPI
import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# OR Create sensor object, communicating over the board's default SPI bus
# spi = board.SPI()
# bmp_cs = digitalio.DigitalInOut(board.D10)
# bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1007.0

while True:
    print("\nTemperature: %0.1f C" % bmp280.temperature)
    temp_f = bmp280.temperature*9/5+32
    print(f"Temperature: {temp_f:0.1f} F")
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    print("Altitude = %0.2f meters" % bmp280.altitude)
    if temp_f >= 125.0:
        with open(Path.cwd().joinpath('EnvironVars/api_key.json'), 'r') as api:
            api_key = json.loads(api.read())
        if api_key['Reported'] == False:
            pb = Pushbullet(api_key['API'])
            push = pb.push_note(f"Temp in battery has exceeded 125!", f"{temp_f:0.2f}")
            api_key['Reported'] = True 
            with open(Path.cwd().joinpath('EnvironVars/api_key.json'), 'w') as api:
                json.dump(api_key, api, indent=4)
    time.sleep(5*60)
