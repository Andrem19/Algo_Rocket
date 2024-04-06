import talib
import shared_vars as sv
from models.cur_pos import Position
from datetime import datetime


def run(data):

    start_index = sv.settings.chunk_len*2
    data_lenth = len(data)
    print(data_lenth, start_index)
    amount = (sv.settings.amount/3) / data[start_index][4]
    print(f'first am: {amount}')
    sv.position = Position(amount, data[start_index][4])
    global_profit = 0
    num = 0
    pause = 0
    i = start_index
    max_lost = 0
    level_3_count = 0
    level_2_count = 0
    while i < data_lenth:
        closes = data[i-sv.settings.chunk_len*2:i, 4]
        # highs = data[i-sv.settings.chunk_len*2:i, 2]
        # lows = data[i-sv.settings.chunk_len*2:i, 3]
        # opens = data[i-sv.settings.chunk_len*2:i, 1]

        res, profit, am_profit = is_profit(sv.position.amount_coin, sv.position.zero_point, closes[-1], 1)
        rsi = talib.RSI(closes, 27)
        if res and sv.position.level != 0:
            global_profit+=profit
            sv.position.amount_coin-=am_profit
            sv.position.zero_point = closes[-1]
            sv.position.level = 1
            if rsi[-1]>77:
                sv.position.level = 0
                sv.position.zero_point = 0
                sv.position.amount_coin = 0
                sv.position.base_amount = 0
                global_profit-=(sv.settings.amount/3)*0.0006
            num+=1
            print(f'-{num} RSI: {round(rsi[-1], 2)} Saldo: {round(profit, 2)} -- {datetime.fromtimestamp(data[i][0]/1000).strftime("%d/%m/%Y")} -- Profit: {global_profit} Level: {sv.position.level}')
        else:
            if pause > 0:
                pause-=1
            if (rsi[-1]<20 and sv.position.level == 1 and pause == 0 and profit < -sv.settings.amount*0.18) or (rsi[-1]<18 and sv.position.level == 2 and pause == 0 and profit < -sv.settings.amount*0.34) or (sv.position.level == 0 and rsi[-1]<34):
                amount = (sv.settings.amount/3) / closes[-1]
                sv.position.amount_coin+=amount
                sv.position.level+=1
                if sv.position.level == 3:
                    level_3_count+=1
                if sv.position.level == 2:
                    level_2_count+=1
                sv.position.zero_point = calc_zero_point(sv.position.amount_coin)
                pause = 100
                num+=1
                print(f'+{num} RSI: {round(rsi[-1], 2)} Saldo: {round(profit, 2)} -- {datetime.fromtimestamp(data[i][0]/1000).strftime("%d/%m/%Y")} -- Profit: {global_profit} Level: {sv.position.level}')
        if profit < max_lost:
            max_lost = profit
        i+=1
    print(f'Max Lost: {max_lost}\nLevel 2: {level_2_count} Level 3: {level_3_count}')
        
        


def calc_zero_point(amount):
    part = sv.settings.amount / 3
    am_usdt = part*sv.position.level
    return am_usdt/amount


def is_profit(amount, zero_point, curr_pr, percent):
    start_sum = zero_point*amount
    cur_sum = curr_pr*amount
    profit = (cur_sum - start_sum)*0.9994
    if profit < ((sv.settings.amount/3)/100*percent):
        return False, profit, 0
    should_left = (sv.settings.amount/3)/curr_pr
    am_profit = amount-should_left
    return True, profit, am_profit


