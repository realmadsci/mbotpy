import time

import mbotpy

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        while True:
            dist = bot.requestUltrasonicSensor()
            print(f'{dist=}')
            bot.doBuzzer(dist * 30, 0.2)
