from card import CARD


def start_give(black, white):
    dict = []
    for i in range(0,2):
        x = CARD('white', white[0], 0)
        dict.append(x)
        white.pop(0)
        y = CARD('black', black[0], 0)
        dict.append(y)
        black.pop(0)
    return sorted(dict, key=elem)

def elem(obj):
    return obj.number, obj.color
