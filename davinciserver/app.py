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
now_turn = ""
racer_guess = {}
status = 0
def init():
    global black
    global white
    global players
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
    now_index = 0
    card_item = CARD(color, number, 0)
    for i in players:
        if (i.name == name):
            i.Hand.append(card_item)
            i.Hand.sort(key=elem)
            for j in i.Hand:
                if j.number != card['number']:
                    now_index += 1
                else:
                    break
    card['now_index'] = now_index
    return json.dumps(card)

@app.route('/show_cards', methods=['get'])
def show():
    cards = {}
    cards['white'] = len(white)
    cards['black'] = len(black)
    return json.dumps(cards)

@app.route('/player_status', methods=['get'])
def player_status():
    if (len(players)>1):
        return "complete"
    else:
        return "not complete"

@app.route('/racer', methods=['get'])
def racer():
    get_data = request.args.to_dict()
    name = get_data.get('name')
    for i in players:
        if (i.name != name):
            return i.name

@app.route('/guess', methods=['get'])
def guess():
    global racer_guess
    global status
    status = 0
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
                i.Hand[int(index)].is_show = 1
                guess_result = 'yes'
                racer_guess['res'] = 'yes'
                racer_guess['guess_number'] = number
                racer_guess['guess_color'] = i.Hand[int(index)].color
                racer_guess['get_card'] = now_index
            else:
                guess_result = 'no'
                racer_guess['res'] = 'no'
                racer_guess['guess_number'] = number
                racer_guess['guess_color'] = i.Hand[int(index)].color
                racer_guess['get_card'] = now_index
            defender_cards = i.show(0)
    for i in players:
        if (attacker == i.name):
            if (guess_result == 'no'):
                i.Hand[int(now_index)].is_show = 1
            attacker_cards = i.show(1)
    res_dict = {}
    res_dict['guess_result'] = guess_result
    res_dict['defender'] = defender_cards
    res_dict['self'] = attacker_cards
    status = 1
    return json.dumps(res_dict)

@app.route('/start', methods=['get'])
def start():
    global now_turn
    get_data = request.args.to_dict()
    name = get_data.get('name')
    ip = get_data.get('ip')
    print(name)
    player = PLAYER(name, ip)
    dict = start_give(black, white)
    for j in dict:
        player.Hand.append(j)
    players.append(player)
    now_turn = name
    #print(now_turn)
    return 'good luck'

@app.route('/show_two', methods=['get'])
def show_two():
    for i in players:
        for j in i.Hand:
            print(j.color, j.number)
    return 'yes'

@app.route('/end_check', methods=['get'])
def end_check():
    temp = 0
    for i in players:
        if i.end_check():
            temp = 1
            break
    if (temp == 1):
        init()
    return str(temp)

@app.route('/show_racer', methods=['get'])
def show_racer():
    get_data = request.args.to_dict()
    name = get_data.get('name')
    res = ""
    for i in players:
        if i.name != name:
            for j in i.Hand:
                if j.is_show:
                    res = res + " " + j.color + " " +str(j.number)
                else:
                    res = res + " " + j.color
    return res

@app.route('/show_my', methods=['get'])
def show_my():
    get_data = request.args.to_dict()
    name = get_data.get('name')
    res = ""
    res1 = ""
    for i in players:
        if i.name == name:
            for j in i.Hand:
                res = res + " " +j.color + " " + str(j.number)
                if j.is_show:
                    res1 = res1 + " " + j.color + " " +str(j.number)
                else:
                    res1 = res1 + " " + j.color
    return res + "\n" +  res1

@app.route('/turn', methods=['get'])
def turn():
    global now_turn
    #print(now_turn)
    return now_turn
@app.route('/racer_guess_res', methods=['get'])
def racer_guess_res():
    global racer_guess
    global status
    if status == 0:
        return '0'
    else:
        return json.dumps(racer_guess)
@app.route('/change_turn', methods=['get'])
def change_turn():
    global now_turn
    get_data = request.args.to_dict()
    name = get_data.get('name')
    for i in players:
        if i.name!=name:
            now_turn = i.name
            status = 0
            break
    return "changed"

if __name__ == '__main__':
    app.run()
