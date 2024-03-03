from models.signal import Signal
import helpers.tools as tools
import talib
import numpy as np
import Indicators.figures as fig
import Indicators.talibr as ta
import helpers.util as util
import shared_vars as sv

def get_signal(i, data):

    closes = data[i-sv.settings.chunk_len*2:i, 4]
    highs = data[i-sv.settings.chunk_len*2:i, 2]
    lows = data[i-sv.settings.chunk_len*2:i, 3]
    opens = data[i-sv.settings.chunk_len*2:i, 1]
    volume = data[i-sv.settings.chunk_len*2:i, 5]
    sg = 3

    #=================START LOGIC===================
    
    rsi = talib.RSI(closes, 22)
    if rsi[-1]>70:
        if closes[-1] < highs[-2] and (closes[-1]>opens[-1] or closes[-1]>opens[-2]): #0.04
            low_tail, high_tail, body = tools.get_tail_body(opens[-2], highs[-2], lows[-2], closes[-2])
            if high_tail > body*0.1:
                low_tail, high_tail, body = tools.get_tail_body(opens[-1], highs[-1], lows[-1], closes[-1])
                if high_tail > body*0.2 and low_tail > body*0.8:
                    if tools.check_high_candel(highs, lows, 0.04, sv.settings.coin):#0.04
                        sg = 2
                        sv.settings.init_stop_loss = 0.004
                        sv.settings.target_len = 5
                        sv.signal.type_os_signal = 'test_1'
                        sv.settings.amount = 20#20



    #=================END LOGIC=====================

    if sg in sv.settings.s:
        sv.signal.signal = sg
        sv.signal.data = sv.settings.time
    else:
        sv.signal.signal = 3
