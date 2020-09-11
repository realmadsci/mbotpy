import time

import mbotpy

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        bot.doMove(0,  1)
        time.sleep(1)
        bot.doMove(0, -1)
        time.sleep(1)
        bot.doMove(1, 0)
        time.sleep(1)
        bot.doMove(-1,  0)
        time.sleep(1)
        bot.doMove(1,  0)
        time.sleep(1)

        for i in range(100):
            bot.doMove(i/100, i/100)
            time.sleep(0.5)
            print(f'{i=}')
        bot.doMove(0, 0)
