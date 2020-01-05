from flask import Flask, request
import random
import json
from player import PLAYER
from card import CARD
from util import *
app = Flask(__name__)

black = list(range(12))
random.shuffle(black)
white = list(range(12))
random.shuffle(white)
players = []


@app.route('/get_card', methods=['get'])
def get_card():
    get_data = request.args.to_dict()
    index = get_data.get('index')
    index = int(index)
    color = get_data.get('color')
    name = get_data.get('name')
    number = '-1'
    if (color == "black"):
        number = black[index]
        black.remove(number)
    elif (color == "white"):
        number = white[index]
        white.remove(number)
    card = {}
    card['number'] = number
    card['color'] = color
    card_item = CARD(color, number, 0)
    for i in players:
        if (i.name == name):
            i.Hand.append(card_item)
            i.Hand.sort(key=elem)
    return json.dumps(card)

@app.route('/show_cards', methods=['get'])
def show():
    cards = {}
    cards['white'] = len(white)
    cards['black'] = len(black)
    return json.dumps(cards)

@app.route('/guess', methods=['get'])
def guess():
    get_data = request.args.to_dict()
    attacker = get_data.get('attacker')
    index = get_data.get('index')
    defender = get_data.get('defender')
    number = get_data.get('number')
    now_index = get_data.get('now_index')
    defender_cards = ""
    attacker_cards = ""
    guess_result = ""
    for i in players:
        print(i.name)
        print(defender)
        if (defender == i.name):
            if (i.attacked(index, number) == 1):
                i.Hand[index].is_show = 1
                guess_result = 'yes'
            else:
                guess_result = 'no'
            defender_cards = i.show(0)
    for i in players:
        if (attacker == i.name):
            if (guess_result == 'no'):
                i.Hand[now_index].is_show = 1
            attacker_cards = i.show(1)

    res_dict = {}
    res_dict['guess_result'] = guess_result
    res_dict[defender] = defender_cards
    res_dict['self'] = attacker_cards
    return json.dumps(res_dict)

@app.route('/start', methods=['get'])
def start():
    get_data = request.args.to_dict()
    name = get_data.get('name')
    ip = get_data.get('ip')
    player = PLAYER(name, ip)
    dict = start_give(black, white)
    for j in dict:
        player.Hand.append(j)
    players.append(player)
    return 'good luck'

@app.route('/show_two', methods=['get'])
def show_two():
    for i in players:
        for j in i.Hand:
            print(j.color, j.number)
    return 'yes'

@app.route('/end_check', methods=['get'])
def end_check():
    temp = 1
    for i in players:
        if not i.end_check():
            temp = 0
            break
    return str(temp)

if __name__ == '__main__':
    app.run()
