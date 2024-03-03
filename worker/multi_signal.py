from models.settings import Settings
import helpers.util as util
from models.signal import Signal
import helpers.func_cointegration as cointegr
import helpers.tools as tools
import statsmodels.api as sm
import talib
import numpy as np
import Indicators.figures as fig
import helpers.util as util
import shared_vars as sv

def get_signal(i_1, i_5, i_15_1, i_15_2, data_1, settings: Settings):
    if sv.gen_increaser.increase_border>0:
        sv.gen_increaser.increase_border-=1
    if sv.adx_counter > 0:
        sv.adx_counter-=1
    if sv.frozen > 0:
        sv.frozen-=1
        sv.signal.signal = 3
        return
    rsi_global = {}
    go_1m = True
    go_5m = True
    go_15m = True

    chunk_len = sv.settings.chunk_len
    closes_1 = data_1[i_1-chunk_len*2:i_1, 4]
    highs_1 = data_1[i_1-chunk_len*2:i_1, 2]
    lows_1 = data_1[i_1-chunk_len*2:i_1, 3]
    opens_1 = data_1[i_1-chunk_len*2:i_1, 1]

    if i_5 == -1:
        go_5m = False
    elif go_5m:
        closes_5 = sv.data_5[i_5-chunk_len*2:i_5, 4]
        highs_5 = sv.data_5[i_5-chunk_len*2:i_5, 2]
        lows_5 = sv.data_5[i_5-chunk_len*2:i_5, 3]
        opens_5 = sv.data_5[i_5-chunk_len*2:i_5, 1]

        # row_1 = serv.chose_arr(0, closes_5[:-10], 10)
        # row_2 = serv.chose_arr(3, closes_5[:-10], 10)

        # sv.trend_up = (all(np.diff(row_1) > 0) or all(np.diff(row_2) > 0))
    
    if i_15_1 == -1 or i_15_2 == -1 or (i_15_1 < 160 or i_15_2 < 160):
        go_15m = False
    elif go_15m:
        closes_15_1 = sv.data_1[i_15_1-chunk_len*2:i_15_1, 4]
        highs_15_1 = sv.data_1[i_15_1-chunk_len*2:i_15_1, 2]
        lows_15_1 = sv.data_1[i_15_1-chunk_len*2:i_15_1, 3]
        opens_15_1 = sv.data_1[i_15_1-chunk_len*2:i_15_1, 1]

        closes_15_2 = sv.data_2[i_15_2-chunk_len*2:i_15_2, 4]
        # sv.btc_15m = closes_15_2
        # sv.other_15m = closes_15_1
        # highs_15_2 = sv.data_2[i_15_2-chunk_len*5:i_15_2, 2]
        # lows_15_2 = sv.data_2[i_15_2-chunk_len*5:i_15_2, 3]
        # opens_15_2 = sv.data_2[i_15_2-chunk_len*5:i_15_2, 1]
    
    

    if go_5m:
        signal_5 = 3

        #====================SIGNAL====================

        low_tail, high_tail, body = tools.get_tail_body(opens_5[-1], highs_5[-1], lows_5[-1], closes_5[-1])
        rsi = talib.RSI(closes_5, 20)
        rsi_global[5]=rsi[-1]
        if rsi[-1]<18: #24
            if tools.check_high_candel(highs_5[-1], lows_5[-1], 0.028, settings.coin) and closes_1[-1] > opens_1[-1] and low_tail < body: #30
                signal_5 = 1
                sv.settings.init_stop_loss = 0.004 #0.004
                sv.settings.target_len = 7#5
                sv.settings.amount = 20#20
                sv.signal.type_os_signal = 'ham_5a'
        
        if signal_5 == 3:
            if rsi[-1]<28: #24
                if tools.check_high_candel(opens_5[-1], closes_5[-1], 0.030, settings.coin) and closes_1[-1] < opens_1[-1] and tools.check_rise(highs_5, lows_5, 2, 10, 'less'): #30
                    comp = tools.all_True_any_False(closes_5, opens_5, 4, 'all', True)
                    if comp:
                        signal_5 = 1
                        sv.settings.init_stop_loss = 0.004 #0.004
                        sv.settings.target_len = 3#3
                        sv.settings.amount = 20#20
                        sv.signal.type_os_signal = 'ham_5b'
                    else:
                        sv.frozen = 3
                        sv.signal.signal = 3
                        return

        if signal_5 == 3:
            op5, hi5, lo5, cl5 = None, None, None, None 
            incline_res_5 = util.calculate_percent_difference(closes_5[-chunk_len], closes_5[-1])
            if abs(incline_res_5) > 0.040:
                signal_5 = tools.pass_step(signal_5, 0.016, 28, opens_5, highs_5, lows_5, closes_5, 5, 27)
                if signal_5 == 1:
                    sv.settings.init_stop_loss = 0.01#0.01
                    sv.settings.amount = 20#20
                    sv.settings.target_len = 7#7
                    sv.signal.type_os_signal = 'rsi_5'
                    if closes_1[-1] > highs_1[-3] or tools.all_True_any_False(closes_1, opens_1, 5, 'all', True):
                        signal_5 = 3
                        sv.signal.signal = 3
                        sv.frozen = 3
                        return
        
        if signal_5 == 3:
            rsi = talib.RSI(closes_5, 32)#32
            if rsi[-1]>30 and rsi[-1] < 50:
                if tools.check_high_candel(highs_5[-2], lows_5[-2], 0.036, sv.settings.coin) and closes_5[-1] > lows_5[-2] and closes_1[-1]< opens_1[-1]:#0.044
                    low_tail, high_tail, body = tools.get_tail_body(opens_5[-2], highs_5[-2], lows_5[-2], closes_5[-2])
                    if low_tail > body*0.4 and opens_5[-2]>closes_5[-2]:#0.4
                        low_tail, high_tail, body = tools.get_tail_body(opens_5[-1], highs_5[-1], lows_5[-1], closes_5[-1])
                        if low_tail > body*0.1 and opens_5[-1]>closes_5[-1] and high_tail < body*0.4:#0.1 0.4
                            if tools.check_high_candel(highs_5[-1], lows_5[-1], 0.018, sv.settings.coin):#0.024
                                signal_5 = 1
                                sv.settings.init_stop_loss = 0.006#0.004
                                sv.settings.amount = 20#20
                                sv.settings.target_len = 20#20
                                sv.signal.type_os_signal = 'mid_5'     

        if signal_5 == 3:
            if tools.check_high_candel(highs_5[-1], lows_5[-1], 0.02, settings.coin) and closes_1[-1] > opens_1[-1] and sv.adx_counter == 0:#18
                adx = talib.ADX(highs_5, lows_5, closes_5, timeperiod=24)
                plus_di = talib.PLUS_DI(highs_5, lows_5, closes_5, timeperiod=24)
                minus_di = talib.MINUS_DI(highs_5, lows_5, closes_5, timeperiod=24)
                rsi = talib.RSI(closes_5, timeperiod=20)

                if plus_di[-1]>50 and rsi[-1]>80 and adx[-1]>46:#50 80 46
                    signal_5 = 2
                    sv.settings.target_len = 10#10
                    sv.settings.init_stop_loss = 0.014#0.014
                    sv.settings.amount = 20
                    sv.signal.type_os_signal = 'adx_5'
                    sv.adx_counter = 14
                

        #====================END SIGNAL================

        if signal_5 in sv.settings.s:
            sv.signal.signal = signal_5
            sv.signal.data = 5
            sv.signal.index = i_1
            return

    if go_1m:
        signal_1 = 3
        op5, hi5, lo5, cl5 = None, None, None, None 
        #====================SIGNAL====================
        rsi = talib.RSI(closes_1, 27)
        rsi_global[1]=rsi[-1]
        if rsi[-1]<20:#18
            if tools.check_high_candel(highs_1[-1], lows_1[-1], 0.020, settings.coin) and closes_1[-1] > opens_1[-1]:
                sv.signal.type_os_signal = 'ham_1a'
                sv.settings.init_stop_loss = 0.004#serv.set_stls(0.020, abs(vol_can))#0.004
                sv.settings.target_len = 5#5
                sv.settings.amount = 20#20
                signal_1 = 1
        
        if rsi[-1]<20:#18
            if tools.check_high_candel(closes_1[-1], opens_1[-1], 0.020, settings.coin) and closes_1[-1] < opens_1[-1]:
                low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])
                sv.signal.type_os_signal = 'ham_1b'
                sv.settings.init_stop_loss = 0.004 #0.004
                sv.settings.target_len = 3#3
                sv.settings.amount = 20#20
                signal_1 = 1
        
        if signal_1 == 3:
            if rsi[-1]<22: #24
                if op5 is None:
                    op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 4)
                low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])
                if tools.check_high_candel(op5[-1], cl5[-1], 0.034, settings.coin) and closes_1[-1] < opens_1[-1] and low_tail > body*0.2 and closes_1[-1]<lows_1[-2]: #32
                        signal_1 = 1
                        sv.settings.init_stop_loss = 0.004 #0.004
                        sv.settings.target_len = 3#3
                        sv.settings.amount = 20#20
                        sv.signal.type_os_signal = 'ham_5bb'
                        

        if signal_1 == 3:
            incline_res_1 = util.calculate_percent_difference(max(highs_1[-chunk_len:]), closes_1[-1])
            incline_res_11 = util.calculate_percent_difference(min(lows_1[-chunk_len:]), closes_1[-1])

            if abs(incline_res_1) > 0.018 or abs(incline_res_11) > 0.018:
                signal_1 = tools.pass_step(signal_1, 0.016, 24, opens_1, highs_1, lows_1, closes_1, 1, 27)
                if signal_1 == 1:
                    sv.settings.init_stop_loss = 0.004#0.004
                    sv.settings.target_len = 3#3
                    sv.signal.type_os_signal = 'rsi_1'
                    sv.settings.amount = 20#20

                    if op5 is None:
                        op5, hi5, lo5, cl5 = tools.convert_timeframe(opens_1, highs_1, lows_1, closes_1, 4)
                    low_tail, high_tail, body = tools.get_tail_body(op5[-1], hi5[-1], lo5[-1], cl5[-1])

                    if tools.all_True_any_False(closes_1, opens_1, 5, 'all', True) or closes_1[-1]<lows_1[-2] or low_tail< body*0.3 or closes_1[-1]< opens_1[-1]:
                        signal_1 = 3
                        sv.gen_increaser.increaser_1.triger = True
                         

        if signal_1 == 3:
            rsi = talib.RSI(closes_1, 32)#32
            if rsi[-1]> 75:#70
                low_tail, high_tail, body = tools.get_tail_body(opens_1[-1], highs_1[-1], lows_1[-1], closes_1[-1])

                comp = tools.all_True_any_False(closes_1, opens_1, 4, 'all', False)#4
                if tools.check_high_candel(closes_1[-1], opens_1[-1], 0.03, settings.coin):
                    trig_1 = closes_1[-1]> opens_1[-1]
                    trig_2 = closes_1[-1]<highs_1[-2]
                    trigger_list = [trig_1, trig_2]
                    if trigger_list.count(True) >= 1 and comp and tools.check_rise(highs_1, lows_1, 2, 3, 'bigger'):
                        signal_1 = 2
                        sv.signal.type_os_signal = 'down_1'
                        sv.settings.init_stop_loss = 0.014#0.004
                        sv.settings.target_len = 7#10
                        sv.settings.amount = 20#20

        #====================END SIGNAL================

        if signal_1 in sv.settings.s:
            sv.signal.signal = signal_1
            sv.signal.data = 1
            sv.signal.index = i_1
            return
    
    if go_15m:
        signal_15 = 3
        op5, hi5, lo5, cl5 = None, None, None, None 

        rsi = talib.RSI(closes_15_1, 22)#22
        rsi_global[15] = rsi[-1]
        if rsi[-1] <28:#28
            max_br = max([opens_15_1[-1], closes_15_1[-1]])
            body = abs(opens_15_1[-1] - closes_15_1[-1])
            high_tail = highs_15_1[-1] - max_br

            min_br = min([opens_15_1[-1], closes_15_1[-1]])
            low_tail = min_br - lows_15_1[-1]
            if closes_1[-1]>opens_1[-5] or (low_tail < body and closes_1[-1]>opens_1[-1]):
                
                if tools.check_high_candel(highs_15_1[-1], lows_15_1[-1], 0.03, settings.coin):#0.01
                # vol_can = abs(serv.calculate_percent_difference(highs_15_1[-1], lows_15_1[-1]))
                # if vol_can > 0.03:
                    model = sm.OLS(closes_15_1, closes_15_2).fit()
                    hedge_ratio = model.params[0]
                    spread = cointegr.calculate_spread(closes_15_1, closes_15_2, hedge_ratio)
                    zscore = cointegr.calculate_zscore(spread, 60)#65

                    if zscore[-1] < -4:
                        signal_15 = 1
                        sv.signal.type_os_signal = 'coint_15'
                        sv.settings.init_stop_loss = 0.01#0.01
                        sv.settings.target_len = 15#29
                        sv.settings.amount = 20#20

        if signal_15 == 3:
            if rsi[-1]< 28:
                if tools.check_high_candel(highs_15_1[-1], lows_15_1[-1], 0.06, settings.coin) and closes_1[-1] < opens_1[-5]:#0.01
                    signal_15 = 1
                    sv.settings.target_len = 5#10
                    sv.settings.init_stop_loss = 0.006#0.006
                    sv.settings.amount = 20
                    sv.signal.type_os_signal = 'ham_15'
        
        if signal_15 == 3:
            rsi = talib.RSI(closes_15_1, 32)
            if rsi[-1]>30 and rsi[-1] < 50:
                if tools.check_high_candel(highs_15_1[-2], lows_15_1[-2], 0.03, sv.settings.coin) and closes_15_1[-1] > lows_15_1[-2]:#0.044
                    low_tail, high_tail, body = tools.get_tail_body(opens_15_1[-2], highs_15_1[-2], lows_15_1[-2], closes_15_1[-2])
                    if low_tail > body*0.8 and opens_15_1[-2]>closes_15_1[-2]:#0.8
                        low_tail, high_tail, body = tools.get_tail_body(opens_15_1[-1], highs_15_1[-1], lows_15_1[-1], closes_15_1[-1])
                        if low_tail > body*0.1 and opens_15_1[-1]>closes_15_1[-1] and high_tail < body*0.8:#0.1 0.8
                            if tools.check_high_candel(highs_15_1[-1], lows_15_1[-1], 0.02, sv.settings.coin):#0.034
                                model = sm.OLS(closes_15_1, closes_15_2).fit()
                                hedge_ratio = model.params[0]
                                spread = cointegr.calculate_spread(closes_15_1, closes_15_2, hedge_ratio)
                                zscore = cointegr.calculate_zscore(spread, 60)#65

                                if zscore[-1] < -2:
                                    signal_15 = 1
                                    sv.settings.init_stop_loss = 0.008#0.008
                                    sv.settings.amount = 20#20
                                    sv.settings.target_len = 20#15
                                    sv.signal.type_os_signal = 'mid_15'   

        
        if signal_15 in sv.settings.s:
            sv.signal.signal = signal_15
            sv.signal.data = 15
            sv.signal.index = i_1
            return


    sv.signal.signal = 3
    return