import talib

def is_hummer(opens, highs, lows, closes):
    hammer = talib.CDLHAMMER(opens, highs, lows, closes)
    if any(hammer[-3:-1] == 100):
        return True
    return False

def is_engulfing(opens, highs, lows, closes):
    patterns = talib.CDLENGULFING(opens, highs, lows, closes)
    if any(patterns[-5:] == 100):
        return True
    return False

def is_hangingman(opens, highs, lows, closes):
    
    hangingman = talib.CDLHANGINGMAN(opens, highs, lows, closes)
    if any(hangingman[-5:] < 0):
        return True
    return False

def is_three_linestrike(opens, highs, lows, closes, up_down):

    three_linestrike = talib.CDL3LINESTRIKE(opens, highs, lows, closes)
    if up_down == 'up':
        if any(three_linestrike[-5:] < 0):
            return True
    if up_down == 'down':
        if any(three_linestrike[-5:] > 0):
            return True
    return False

def is_three_black_crows(opens, highs, lows, closes):
    black_crows_patterns = talib.CDL3BLACKCROWS(opens, highs, lows, closes)

    if black_crows_patterns[-1] != 0:
        return True
    return False

def is_three_white_soldiers(opens, highs, lows, closes):
    white_soldiers_patterns = talib.CDL3WHITESOLDIERS(opens, highs, lows, closes)

    if white_soldiers_patterns[-1] != 0:
        return True
    return False

def is_morning_star(opens, highs, lows, closes): 

    morning_star = talib.CDLMORNINGSTAR(opens, highs, lows, closes)

    if morning_star[-1] == 100:
        return True
    return False