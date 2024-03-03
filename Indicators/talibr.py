import talib
import shared_vars as sv
import numpy as np
from models.increaser import GeneralIncreaser

def rsi_increaser(increaser: GeneralIncreaser, closes, rsi_min_border, timeperiod):

    rsi = talib.RSI(closes, timeperiod=timeperiod)
    if increaser.increase_border> 0:
        rsi_min_border-=increaser.increase_border*2

    if rsi[-1] < rsi_min_border:
        return 1, rsi[-2]
    else:
        return 3, rsi[-2]


    
    
def williams_r(highs, lows, closes):
    willr = talib.WILLR(highs, lows, closes, 42)
    
    signal = 3
    if willr[-1] == 0:
        signal = 2
    elif willr[-1] < -98:
        signal = 1
    else:
        signal = 3

    return signal


def stochastic(highs, lows, closes):
    slowk, slowd = talib.STOCH(highs, lows, closes, fastk_period=20, slowk_period=3, slowd_period=3)
    
    if slowk[-1] < 3 and slowd[-1] < 3:
        return 1
    elif slowk[-1] > 97 and slowd[-1] > 97:
        return 2
    else:
        return 3

def support_resistance(highs, lows, closes):
    support = talib.SMA(lows, 20)
    resistance = talib.SMA(highs, 20)
    if closes[-1] < support[-1] and closes[-2] > support[-2]:
        return 2
    elif closes[-1] > resistance[-1] and closes[-2] < resistance[-2]:
        return 1
    elif closes[-1] <= support[-1]:
        return 1
    elif closes[-1] >= resistance[-1]:
        return 2
    else:
        return 3

def bollinger(closes, highs, lows):
    upper_band, middle_band, lower_band = talib.BBANDS(closes, timeperiod=40)

    last_middle_band = middle_band[-1]
    last_upper_band = upper_band[-1]
    last_lower_band = lower_band[-1]
    last_close = closes[-1]
    last_high = highs[-1]
    last_low = lows[-1]

    if last_high > last_upper_band:
        return 2
    elif last_low < last_lower_band:
        return 1
    else:
        return 3

def natr(high, low, close):
    natr = talib.NATR(high, low, close)

    if natr[-1] > 0.6:
        return 1
    elif natr[-1] < 0.4:
        return 2
    else:
        return 3
    
def detect_trend(highs, lows, closes, adx_trh, rsi_trh, di_trh):
    # Вычисляем индикаторы
    adx = talib.ADX(highs, lows, closes, timeperiod=24)
    plus_di = talib.PLUS_DI(highs, lows, closes, timeperiod=24)
    minus_di = talib.MINUS_DI(highs, lows, closes, timeperiod=24)
    rsi = talib.RSI(closes, timeperiod=20)

    if plus_di[-1]>di_trh and rsi[-1]>rsi_trh and adx[-1]>adx_trh:
        return 2
    # elif adx[-1] > adx_trh_l and rsi[-1]>rsi_trh_l and minus_di[-1]>di_trh_l:
    #     return 1
    return 3

def adx(highs, lows, closes, adx_threshold):
    n = 20
    adx = talib.ADX(highs, lows, closes, timeperiod=n)
    plus_di = talib.PLUS_DI(highs, lows, closes, timeperiod=n)
    minus_di = talib.MINUS_DI(highs, lows, closes, timeperiod=n)

    last_idx = len(adx) - 1

    if plus_di[last_idx] > minus_di[last_idx] and adx[last_idx] > adx_threshold:
        return 1
    elif plus_di[last_idx] < minus_di[last_idx] and adx[last_idx] > adx_threshold:
        return 2
    else:
        return 3
    
def cci(highs, lows, closes):
    cci = talib.CCI(highs, lows, closes, 27)

    signal = 3
    if cci[-1] > 400:
        signal = 2
    elif cci[-1] < -400:
        signal = 1
    else:
        signal = 3

    return signal

    
def mfi(highs, lows, closes, volumes):
    mfi = talib.MFI(highs, lows, closes, volumes)

    signal = 3
    if mfi[-1] > 97:
        signal = 2
    elif mfi[-1] < 3:
        signal = 1
    else:
        signal = 3

    return signal

def demarker(highs, lows):
    n=50
    DeMax = np.maximum(highs[1:] - highs[:-1], 0)
    DeMin = np.maximum(lows[:-1] - lows[1:], 0)

    SMA_DeMax = np.sum(DeMax[-n:]) / n
    SMA_DeMin = np.sum(DeMin[-n:]) / n

    DEM = SMA_DeMax / (SMA_DeMax + SMA_DeMin)

    if DEM > 0.92:
        signal = 2
    elif DEM < 0.08:
        signal = 1
    else:
        signal = 3

    return signal



def obv(closes, volumes):
    obv = talib.OBV(closes, volumes)
    signal = 3

    if obv[-1] > obv[-2] and obv[-2] < obv[-3]:
        signal = 1

    elif obv[-1] < obv[-2] and obv[-2] > obv[-3]:
        signal = 2

    return signal
    
def obv_sma(closes, volumes):
    obv = talib.OBV(closes, volumes)
    obv_sma = talib.SMA(obv, timeperiod=27)

    if obv_sma[-1] > obv_sma[-2] and obv_sma[-1] > volumes[-1]*400:
        return 1
    elif obv_sma[-1] < obv_sma[-2] and obv_sma[-1] < -volumes[-1]*400:
        return 2
    else:
        return 3

def sma_ema(closes):
    sma = talib.SMA(closes, 20)
    ema = talib.EMA(closes, 20)
    
    last_sma = sma[-1]
    last_ema = ema[-1]

    if last_sma > last_ema:
        return 1
    elif last_sma < last_ema:
        return 2
    else:
        return 3

def macd(closes):
    
    macd, signal, _ = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    
    last_macd = macd[-1]
    last_signal = signal[-1]

    if last_macd > last_signal:
        return 1
    if last_macd < last_signal*10000:
        return 2
    else:
        return 3
    
def trend(closes):
    def chose_arr(start_ind: int, arr: np.ndarray, step: int):
        new_arr = []
        for i in range(start_ind, len(arr), step):
            new_arr.append(arr[i])
        return np.array(new_arr)
    closes = closes[10:]
    new_arr_1 = chose_arr(0, closes, 10)
    new_arr_2 = chose_arr(2, closes, 10)
    new_arr_3 = chose_arr(4, closes, 10)
    new_arr_4 = chose_arr(6, closes, 10)
    if all(np.diff(new_arr_1) > 0) or all(np.diff(new_arr_2) > 0) or all(np.diff(new_arr_3) > 0) or all(np.diff(new_arr_4) > 0):
        return 3  # тренд вверх
    elif all(np.diff(new_arr_1) < 0) or all(np.diff(new_arr_2) < 0) or all(np.diff(new_arr_3) < 0) or all(np.diff(new_arr_4) < 0):
        return 2  # тренд вниз
    else:
        return 3  # нет тренда
    
def average_true_range(highs, lows, closes):
    atr = talib.ATR(highs, lows, closes, timeperiod=14)
    return atr

def commodity_channel_index(highs, lows, closes):
    cci = talib.CCI(highs, lows, closes, timeperiod=14)
    return cci

def rate_of_change(closes):
    roc = talib.ROC(closes, timeperiod=10)
    return roc

def pivot_points(highs, lows, closes):
    pivot = (highs[-1] + lows[-1] + closes[-1]) / 3

    r1 = 2 * pivot - lows[-1]
    s1 = 2 * pivot - highs[-1]
    r2 = pivot + (highs[-1] - lows[-1])
    s2 = pivot - (highs[-1] - lows[-1])
    return pivot, r1, s1, r2, s2

