import requests
import socket
import time
import json
start_status = 0
myname = socket.gethostname()
ip = socket.gethostbyname(myname)
while (1):
    if (start_status == 0):
        name = input("please input your name:")
        r = requests.get('http://127.0.0.1:5000/start', data = {'name': name,'ip':ip})
        if (r.status_code == 200):
            another_player_status = 0
            x = 0
            while (another_player_status == 0):
                req = requests.get('http://127.0.0.1:5000/player_status')
                if req.text == 'complete':
                    print('good luck to you')
                    another_player_status = 1
                    break
                print('good luck to you, please wait another player' + '.' * x, end = " ", flush=True)
                x = (x+1) % 4
                time.sleep(1)
            if (another_player_status == 1):
                color = input("please choose white or black card to get, input white or black")
                index = input("please choose index of white or black cards, input the number")
                req = requests.get('http://127.0.0.1:5000/get_card', data = {'color':color, 'index':index, 'name':name})
                card = json.loads(req.text)
                print('your card is ' + card['color'] + ":" + card['number'])
                req = requests.get('http://127.0.0.1:5000/show_my', data={'name':name})
                print('your cards list is now ' + req.text)

