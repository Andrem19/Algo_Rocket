import helpers.util as util
import numpy as np
import high_koff as hk
import talib
import coins_2
import shared_vars as sv
from models.increaser import Increaser
from models.increaser import GeneralIncreaser
from numba import jit


def last_close_higher(highs, lows, closes, lower_higher, high_low_tail):
    if lower_higher == 'none':
        return True
    elif lower_higher == 'lower':
        if high_low_tail == 'high':
            return closes[-1]<highs[-2]
        else:
            return closes[-1]<lows[-2]
    elif lower_higher == 'higher':
        if high_low_tail == 'high':
            return closes[-1]>highs[-2]
        else:
            return closes[-1]>lows[-2]
    return False


def check_rsi(closes, timestep, min_level, max_level):
    
    rsi = talib.RSI(closes, timestep)
    current_rsi = rsi[-1]
    
    within_min = current_rsi > min_level if min_level > 0 else True
    within_max = current_rsi < max_level if max_level > 0 else True

    return within_min and within_max
    
def open_close(open1, close1, lower_bigger):
    if lower_bigger == 'none':
        return True
    if lower_bigger == 'lower':
        return close1<open1
    else:
        return close1>open1


def trend(closes: np.ndarray, variant: str, step: int, minus_last: int):
    row_1 = util.chose_arr(0, closes[:-minus_last], step)
    row_2 = util.chose_arr(3, closes[:-minus_last], step)
    row_3 = util.chose_arr(6, closes[:-minus_last], step)
    trend = False
    if variant == 'up':
        trend = all(np.diff(row_1) > 0) or all(np.diff(row_2) > 0) or all(np.diff(row_3) > 0)
    elif variant == 'down':
        trend = all(np.diff(row_1) < 0) or all(np.diff(row_2) < 0) or all(np.diff(row_3) < 0)
    elif variant == 'none':
        trend_1 = all(np.diff(row_1) > 0) or all(np.diff(row_2) > 0) or all(np.diff(row_3) > 0)
        trend_2 = all(np.diff(row_1) < 0) or all(np.diff(row_2) < 0) or all(np.diff(row_3) < 0)
        trend = not trend_1 and not trend_2
    
    return trend

def what_trend(closes: np.ndarray, step: int, minus_last: int):
    if len(closes) < 60:
        return 'none'
    row_1 = util.chose_arr(0, closes[:-minus_last], step)
    row_2 = util.chose_arr(3, closes[:-minus_last], step)
    row_3 = util.chose_arr(6, closes[:-minus_last], step)
    trend = False

    trend_up = all(np.diff(row_1) > 0) or all(np.diff(row_2) > 0) or all(np.diff(row_3) > 0)

    trend_down = all(np.diff(row_1) < 0) or all(np.diff(row_2) < 0) or all(np.diff(row_3) < 0)

    if trend_up:
        return 'up'
    elif trend_down:
        return 'down'
    else:
        return 'none'


def check_rise(highs: np.ndarray, lows: np.ndarray, numval: int, multiplier: float, less_bigger: str):
    num = numval+1
    high = highs[-num:]
    low = lows[-num:]

    comparisons = high - low

    median = (sum(comparisons[-num:-1])/len(comparisons[-num:-1]))*multiplier

    res = False
    if less_bigger == 'less':
        if comparisons[-1] < median:
            res = True
        else:
            res = False
    elif less_bigger == 'bigger':
        if comparisons[-1] > median:
            res = True
        else:
            res = False
    return res

@jit(nopython=True)
def all_True_any_False(closes: np.ndarray, opens: np.ndarray, numval: int, variant: str, types: bool) -> bool:
    num = numval+1
    closes = closes[-num:-1]
    opens = opens[-num:-1]

    comparisons = closes < opens

    if variant == 'any':
        if types:
            return np.any(comparisons)
        else:
            return np.any(~comparisons)
    elif variant == 'all':
        if types:
            return np.all(comparisons)
        else:
            return np.all(~comparisons)

@jit(nopython=True)
def convert_timeframe(opens: np.ndarray, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, timeframe: int, ln: int):
    lenth_opens = len(opens)
    length = lenth_opens // timeframe if ln == 0 else ln

    new_opens = np.zeros(length)
    new_highs = np.zeros(length)
    new_lows = np.zeros(length)
    new_closes = np.zeros(length)

    for i in range(length):
        start = lenth_opens - (i + 1) * timeframe
        end = lenth_opens - i * timeframe

        new_opens[-(i + 1)] = opens[start]
        new_highs[-(i + 1)] = np.max(highs[start:end])
        new_lows[-(i + 1)] = np.min(lows[start:end])
        new_closes[-(i + 1)] = closes[end - 1]

    return new_opens, new_highs, new_lows, new_closes

def position_entry_manager(increaser_gen: GeneralIncreaser, data: int, signal: int) -> int:
    increaser: Increaser = increaser_gen.increaser_1 if data == 1 else increaser_gen.increaser_5 if data == 5 else increaser_gen.increaser_15
    if increaser.offon>0 and signal == 1 and increaser.triger==False:
        increaser_gen.increase_border = 5 if data == 1 else 10 if data == 5 else 15
        increaser.triger=True
        return 3
    elif increaser.offon>0 and increaser.triger==True and signal ==1:
        increaser.triger=False
        return signal
    
    if increaser.offon == 0 and signal == 1:
        increaser.offon = 25
        return 3
    elif increaser.offon > 0:
        increaser.offon-=1
        if increaser.offon == 0:
            increaser.triger=False
    
    return 3

def check_high_candel(high: float, low: float, border, coin: str = 'XRPUSDT'):
    vol_can = util.calculate_percent_difference(high, low)
    if abs(vol_can) > border*coins_2.best_set_dict[coin]:
        return True
    return False

def low_high_tails(open, high, low, close, low_high, lower_bigger, koff):
    if low_high == 'none':
        return True
    low_tail, high_tail, body = get_tail_body(open, high, low, close)
    if low_high == 'low':
        if lower_bigger == 'lower':
            return low_tail<body*koff
        elif lower_bigger == 'bigger':
            return low_tail>body*koff
    elif low_high == 'high':
        if lower_bigger == 'lower':
            return high_tail<body*koff
        elif lower_bigger == 'bigger':
            return high_tail>body*koff

def get_tail_body(open, high, low, close):
    body = abs(open - close)
    min_br = min([open, close])
    low_tail = min_br - low
    max_br = max([open, close])
    high_tail = high - max_br
    return low_tail, high_tail, body

def tail_body(tail, body, lower_bigger, koff):
    if lower_bigger == 'lower':
        return tail < body *koff
    elif lower_bigger == 'bigger':
        return tail > body *koff
    return False

def pass_step(sg: int, vol_cand, br_val, opens, highs, lows, closes, time_frame, time_period):
    if sg != 3 :
        return sg
    min_br = min([opens[-1], closes[-1]])
    body = abs(opens[-1] - closes[-1])
    low_tail = min_br - lows[-1]

    if check_high_candel(highs[-1], lows[-1], vol_cand, sv.settings.coin):
        br = br_val
        if low_tail > body*0.4:
            br = 26
        sg, rsi_2 = rsi_inc_bord(closes,sv.gen_increaser.increase_border, br, time_period)
        if low_tail > body*0.2 and sg == 3 and rsi_2 < 22:
            sg = 1
    
    res_sg = position_entry_manager(sv.gen_increaser, time_frame, sg)
    return res_sg

def rsi_inc_bord(closes, incresce, rsi_min_border, timeperiod):
    rsi = talib.RSI(closes, timeperiod=timeperiod)
    if incresce> 0:
        rsi_min_border-=incresce*2
    if rsi[-1] < rsi_min_border:
        return 1, rsi[-2]
    else:
        return 3, rsi[-2]
    
def down_line(lows, period, treshold):
    per = lows[-period:-1]
    last_point = lows[-1]
    low_border = last_point * (1-treshold*2)
    high_border = last_point * (1+treshold)
    if any(p for p in per if p > low_border and p <high_border and min(per)==p):
        return True
    else:
        return False
    
def up_line(highs, period, treshold):
    per = highs[-period:-1]
    last_point = highs[-1]
    low_border = last_point * (1-treshold)
    high_border = last_point * (1+treshold)
    if any(p for p in per if p > low_border and p <high_border):
        return True
    else:
        return False
    
def up_line_plus(highs, period, treshold):
    per = highs[-period:]
    last_point = highs[-1]
    low_border = last_point * (1-treshold)
    high_border = last_point * (1+treshold)
    if all(p for p in per if p > low_border and p <high_border):
        return True
    else:
        return False
        
def gap_detection(prev_close: float, last_open: float, up_down: str, perc: float):
    if up_down == 'up':
        if last_open > prev_close:
            diff = abs(util.calculate_percent_difference(last_open, prev_close))
            if diff > perc:
                return True
    elif up_down == 'down':
        if last_open < prev_close:
            diff = abs(util.calculate_percent_difference(last_open, prev_close))
            if diff > perc:
                return True
    elif up_down == 'or':
        diff = abs(util.calculate_percent_difference(last_open, prev_close))
        if diff > perc:
            return True
    return False

def return_the_higest_candel(highs: np.ndarray, lows: np.ndarray, opens: np.ndarray, closes: np.ndarray, lenth: int):
    max_index = highs[-lenth:].argmax()
    return opens[max_index], highs[max_index], lows[max_index], closes[max_index]

@jit(nopython=True)
def last_lowest(lows: np.ndarray, lenth: int):
    min_in_last_20 = np.min(lows[-lenth:])
    return lows[-1] == min_in_last_20

@jit(nopython=True)
def last_highest(highs: np.ndarray, lenth: int):
    min_in_last_20 = np.max(highs[-lenth:])
    return highs[-1] == min_in_last_20

@jit(nopython=True)
def last_lowest_highest(highs, lows, lowest_highest_none, ln):
    if lowest_highest_none == 'none':
        return True
    elif lowest_highest_none == 'lowest':
        return last_lowest(lows, ln)
    elif lowest_highest_none == 'highest':
        return last_highest(highs, ln)