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
    # volume = data[i-sv.settings.chunk_len*2:i, 5]
    sg = 3

    #=================START LOGIC===================
    
    sg = sv.reactor.call(sg, opens, highs, lows, closes)



    #=================END LOGIC=====================

    if sg in sv.settings.s:
        sv.signal.signal = sg
        sv.signal.data = sv.settings.time
        sv.settings.init_stop_loss = 0.006 #0.004
        sv.settings.target_len = 3#3
        sv.settings.amount = 20#20
        sv.signal.type_os_signal = 'test_5'
    else:
        sv.signal.signal = 3
