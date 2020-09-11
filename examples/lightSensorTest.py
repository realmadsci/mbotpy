import time

import mbotpy

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        while True:
            light = bot.requestLight(6)
            print(f'{light=}')
            time.sleep(0.2)
