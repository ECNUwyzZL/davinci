# -*- coding: utf-8 -*-
import requests
import socket
import time
from config import SERVER_IP
import json
from util import *
start_status = 0
myname = socket.gethostname()
ip = socket.gethostbyname(myname)
another_player_status = 0
while (1):
    if (start_status == 0 and another_player_status == 0):
        name = input("please input your name:\n")
        data = {'name': name, 'ip': ip}
        r = requests.get(SERVER_IP+'start', params=data)
        if (r.status_code == 200):
            x = 0
            while (another_player_status == 0):
                req = requests.get(SERVER_IP+'player_status')
                if req.text == 'complete':
                    print('good luck to you')
                    another_player_status = 1
                    break
                print('\rgood luck to you, please wait another player' + '.' * x, end = " ", flush=True)
                x = (x+1) % 4
                time.sleep(1)
            if (another_player_status == 1):
                while (check_end()=='0'):
                    if (turn_check(name) == 1):
                        step1 = get_card(name)
                        temp = 0
                        step2 = guess(name,step1)
                        if (step2!='yes'):
                            res = change_turn(name)
                        while (step2 =='yes' and temp == 0 and check_end()=='0'):
                            will = input("Do you want to continue input yes or no\n")
                            if (will=='no'):
                                res = change_turn(name)
                                temp = 1
                            else:
                                step2 = guess(name, step1)
                        if (check_end()=='1'):
                            print("you win!!")
                    else:
                        racer_res = racer_guess(name)



