import time

import mbotpy

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        while True:
            line = bot.requestLineFollower()
            print(f'{line=}')
            time.sleep(0.2)
