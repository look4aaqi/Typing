import sys
class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        
        return chr(int.from_bytes(msvcrt.getch(),sys.byteorder))


getch = _Getch()

import pickle

with open('letters.data', 'rb') as filehandle:
    # read the data as binary data stream
    letters = pickle.load(filehandle)
    

with open('probability.data', 'rb') as filehandle:
    # read the data as binary data stream
    probability = pickle.load(filehandle)


def textGenerator_Letters(length):
    import random
    
    # text = random.choices(letters,weights=probability, k=length)
    # text = [x for x in text if (x.isalpha() or x in (' ', '.', ',','/',':') or x in "1234567890")]
    # text = ''.join(text)

    letters = "!@#$^&*()"
    text = ""
    for i in range(length):
        text += random.choice(letters)

    
    return text

def paraGenerator():
    from essential_generators import DocumentGenerator
    gen = DocumentGenerator()
    import re
    text = gen.sentence()#.lower()
    text = [x for x in text if (x.isalpha() or x in (' ', '.', ',','/',':') or x in "1234567890")]
    text = ''.join(text)
    return text
   
# text = textGenerator_Letters(length=100) + "|"
text = paraGenerator() +  "|"
print(text)
input = ""
ptr = 0


while ptr < (len(text)-1):
    char = getch()
    if char == text[ptr]:
        input += char
        ptr += 1
        print(input, end="\r")
    else:
        ind = letters.index(text[ptr])
        probability[ind] += 0.001
        reduction = 0.001/len(probability)
        for x in range(len(probability)):
            if x != ind:
                probability[x] -= reduction

        print(input + char + ":(", end="\r")
        backspace = getch()
        while ord(backspace) != 8:
            backspace = getch()
        print(input+"   ", end="\r")

print("\nAll Correct")


with open('probability.data', 'wb') as filehandle:
    pickle.dump(probability, filehandle)
    print("Updated weights")

zipped = list(zip(letters, probability))
zipped.sort(key=lambda x:x[1],reverse=True)
print(zipped[:10])
