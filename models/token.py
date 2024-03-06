import helpers.tools as tools
import helpers.util as util
import shared_vars as sv
import talib

token_model = {
    'high<>body*0.6': ['less', 'bigger'],
    'low<>body*0.6': ['less', 'bigger'],
    'cndl_not_less': ['1', '2', '3', '4', '5', '6'],
    'glob1htrend15': ['up', 'down', 'none'],
    'close>prevLow': [True, False],
    'close<prevHigh': [True, False],
    'last1m': ['long', 'short'],
    'rsi': ['>70', '<30', '<70>30'],
    'rise2mult3': ['less', 'bigger'],
    'all_True_any_False_3': ['allDown', 'allUp', 'none'],
    'sccess': 0,
    'fail':0,
}

def decode(opens, highs, lows, closes, last1m_pat):
    pattern = {}
    low_tail, high_tail, body = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
    pattern['high<>body*0.6'] = 'less' if high_tail < body*0.6 else 'bigger'
    pattern['low<>body*0.6'] = 'less' if low_tail < body*0.6 else 'bigger'
    high_cand = int(util.calculate_percent_difference(highs[-1], lows[-1]))
    pattern['cndl_not_less'] = '6' if high_cand > 6 else '1' if high_cand < 2 else str(high_cand)
    pattern['glob1htrend15'] = tools.what_trend(sv.close_60, 15, 5)
    pattern['close>prevLow'] = True if closes[-1] > lows[-2] else False
    pattern['close<prevHigh'] = True if closes[-1] < highs[-2] else False
    pattern['last1m'] = last1m_pat
    rsi = talib.RSI(closes, 27)[-1]
    pattern['rsi'] = '>70' if rsi > 70 else '<30' if rsi < 30 else '<70>30'
    rise_less = tools.check_rise(highs, lows, 2, 3, 'less')
    rise_bigger = tools.check_rise(highs, lows, 2, 3, 'bigger')
    pattern['rise2mult3'] = 'less' if rise_less else 'bigger' if rise_bigger else 'none'
    all_down = tools.all_True_any_False(closes, opens, 3, 'all', True)
    all_up = tools.all_True_any_False(closes, opens, 3, 'all', False)
    pattern['all_True_any_False_3'] = 'allDown' if all_down else 'allUp' if all_up else 'none'
    return pattern

def compare(pattern_1, pattern_2):
    for key, val in pattern_1.items():
        if pattern_1[key] in ['success', 'fail']:
            continue
        if pattern_1[key]!= pattern_2[key]:
            return False
    return True

def check_pattern_1(open, high, low, close, low_tail_border, up_body):
    if close < open:
        return False
    min_br = min([open, close])
    if abs(util.calculate_percent_difference(min_br, low)) > low_tail_border:
        return False
    if abs(util.calculate_percent_difference(open, close)) < up_body:
        return False
    return True

def proccess_data(list_patterns: list, pattern_2: dict, case: bool):
    for pattern_1 in list_patterns:
        if compare(pattern_1, pattern_2):
            if case:
                pattern_1['success']+=1
                break
            else:
                pattern_1['fail']+=1
                break
    if case:
        pattern_2['success']=1
        pattern_2['fail']=0
    else:
        pattern_2['fail']=1
        pattern_2['success']=0
    list_patterns.append(pattern_2)
    

