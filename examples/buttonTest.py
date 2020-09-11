import time

import mbotpy

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        while True:
            b = bot.requestButtonOnBoard()
            print(f'{b=}')
            time.sleep(0.2)
