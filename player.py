# -*- coding: utf-8 -*-
from card import CARD

class PLAYER(object):
    def __init__(self, name, ip):
        self._name = name
        self._ip = ip
        self._Hand = []
        self._score = 0
    @property
    def name(self):
        return self._name

    @property
    def Hand(self):
        return self._Hand

    @property
    def ip(self):
        return self._ip

    def check(self, index):
        return self._Hand[index].is_show

    def add(self, card):
        self._Hand.append(card)

    def attacked(self, index, number):
        if (int(self._Hand[int(index)].number) == int(number)):
            return 1
        else:
            return 0

    def end_check(self):
        temp = 1
        for item in self._Hand:
            if item.is_show == 0:
                temp = 0
                break
        return temp

    def show(self, is_self):
        cards = ""
        if (is_self == 0):
            for i in self._Hand:
                if (i.is_show == 1):
                    cards += i.color + " " + i.number + " "
                else:
                    cards += i.color
            return cards
        else:
            for i in self._Hand:
                cards += i.color + " " + i.number + " "
            return cards





