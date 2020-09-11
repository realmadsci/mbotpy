import time

import mbotpy

tones = {
    "PAUSE": 0,
    "C3":131,"D3":147,"E3":165,"F3":175,"G3":196,"A3":220,"B3":247,
    "C4":262,"C#4":277,"D4":294,"E4":330,"F4":349,"F#4":370,"G4":392,"A4":440,"B4":494,
    "C5":523,"C#5":554,"D5":587,"E5":659,"F5":698,"F#5":740,"G5":784,"A5":880,"B5":988
}

note_times = {
    '1' : 1.6,
    '2' : 0.8,
    'YEET' : 1.6*3/4,
    '4' : 0.4,
    '8' : 0.2
}

def playNote(bot, name, length):
    t = note_times[length]
    print(f'{name=}, {length=}, {t=}')
    bot.doBuzzer(tones[name], t)

if __name__ == '__main__':
    with mbotpy.openSerial("COM4") as bot:
        line1 = '''
        D4/8 E4/8 D4/8 F#4/4 A4/8
        D5/4 F#5/8 E5/8 C#5/8 A4/8
        G4/4 B4/8 F#4/4 A4/8
        E4/4 F#4/8 G4/8 F#4/8 E4/8
        D4/8 E4/8 D4/8 F#4/4 A4/8
        D5/4 F#5/8 E5/8 C#5/8 A4/8
        B4/8  G5/8 F#5/8 E5/8 D5/8 C#5/8
        D5/YEET PAUSE/4 '''

        line2 = '''
        F#5/8 
        A5/4 F#5/8 D5/4 E5/8 
        F#5/4 G5/8 A5/8 G5/8 F#5/8
        G5/4 E5/8 C#5/8 D5/8 E5/8
        E5/4 F#5/8 G5/8 F#5/8 E5/8 
        '''
        ending1 = '''
        A5/4 F#5/8 D5/4 E5/8 
        F#5/4 G5/8 A5/8 G5/8 F#5/8
        G5/4 F#5/8 C#5/8 D5/8 E5/8
        D5/YEET
        '''
        ending2 = '''
        F#5/8 E5/8 D5/8 G5/8 F#5/8 E5/8
        A5/8 G5/8 F#5/8 B5/8 A5/8 G5/8 
        F#5/8 E5/8 D5/8 C#5/8 D5/8 E5/8
        D5/YEET
        '''

        music = line1 + line1 + line2 + ending1 + line2 + ending2

        for note in music.split():
            (n, t) = note.split('/')
            playNote(bot, n, t)
