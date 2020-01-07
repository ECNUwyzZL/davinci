import requests
import json
from config import SERVER_IP
def change_turn(name):
    data = {'name': name}
    req = requests.get(SERVER_IP+'change_turn',params=data)
    return req.text
def check_end():
    req = requests.get(SERVER_IP+'end_check')
    return req.text
def turn_check(name):
    req = requests.get(SERVER_IP+'turn')
    if req.text == name:
        return 1
    else:
        return 0
def get_card(name):
    color = input("please choose white or black card to get, input white or black\n")
    index = input("please choose index of white or black cards, input the number\n")
    data = {'color': color, 'index': index, 'name': name}
    req = requests.get(SERVER_IP+'get_card', params=data)
    card = json.loads(req.text)
    print('your card is ' + card['color'] + ":" + str(card['number']))
    data = {'name': name}
    req = requests.get(SERVER_IP+'show_my', params=data)
    print('your cards list is now\n' + req.text)
    return card['now_index']
def guess(name,step1):
    data = {'name': name}
    req = requests.get(SERVER_IP+'racer',params=data)
    racer = req.text
    print("your racer is " + racer)
    data = {'name': name}
    req = requests.get(SERVER_IP+'show_racer',params=data)
    print("your racer cards are\n" + req.text)
    index = input("please choose the index of card you want to guess\n")
    number = input("please choose a number you guess\n")
    data = {'attacker': name, 'defender': racer, 'index': index, 'number': number, 'now_index': step1}
    req = requests.get(SERVER_IP+'guess', params=data)
    res = json.loads(req.text)
    print("guess result  "+ res['guess_result'])
    print("defender cards\n" + res['defender'])
    data = {'name': name}
    req = requests.get(SERVER_IP+'show_my', params=data)
    print('your cards list is now\n' + req.text)
    return res['guess_result']
def racer_guess(name):
    req = requests.get(SERVER_IP+'racer_guess_res')
    if req.text == '0':
        return '0'
    else:
        res = json.loads(req.text)
        print('your racer guess result is '+res['res'])
        print('your racer guess number is '+res['guess_number'])
        print('your racer guess color is '+res['guess_color'])
        data = {'name': name}
        req = requests.get(SERVER_IP + 'show_racer', params=data)
        print("your racer cards are\n" + req.text)
        print('your racer latest card index is '+res['get_card'])
        return '1'

