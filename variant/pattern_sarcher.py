import shared_vars as sv
import helpers.get_data as gd
import helpers.util as util
import models.token as tok
import talib
import helpers.tools as tools
import numpy as np


async def search_pattern(coin_list):
    coin_len = len(coin_list)
    for c in coin_list:
        print(coin_len)
        coin_len-=1
        sv.settings.coin = c
        sv.data_1 = gd.load_data_sets(1)
        sv.data_5 = gd.load_data_sets(5)
        sv.candel_dict_5 = util.create_candle_dict(sv.data_5)
        sv.data_15 = gd.load_data_sets(15)
        sv.candle_dict_15 = util.create_candle_dict(sv.data_15)
        sv.data_60 = gd.load_data_sets(60)
        sv.candle_dict_60 = util.create_candle_dict(sv.data_60)

        data_len = len(sv.data_1)
        data_len_for_loop = data_len - max(3*15, 5*5)+1
        i_1 = sv.settings.chunk_len*10+1

        while i_1 < data_len_for_loop:
            # i_5 = util.get_candel_index(sv.data_1[i_1][0], sv.candel_dict_5)
            # i_15 = util.get_candel_index(sv.data_1[i_1][0], sv.candle_dict_15)
            i_60 = util.get_candel_index(sv.data_1[i_1][0], sv.candle_dict_60)

            if i_60 != -1 and i_60>60:
                sv.close_60 = sv.data_60[i_60-sv.settings.chunk_len*2:i_60, 4]
            

            closes_1 = sv.data_1[i_1-sv.settings.chunk_len*2:i_1, 4]
            highs_1 = sv.data_1[i_1-sv.settings.chunk_len*2:i_1, 2]
            lows_1 = sv.data_1[i_1-sv.settings.chunk_len*2:i_1, 3]
            opens_1 = sv.data_1[i_1-sv.settings.chunk_len*2:i_1, 1]


            case = tok.check_pattern(sv.data_1[i_1][1], sv.data_1[i_1][2], sv.data_1[i_1][3], sv.data_1[i_1][4], 0.004, 0.008)
            if case == 'none':
                i_1+=1
                continue
            pat1m = 'long' if closes_1[-1]>opens_1[-1] else 'short'
            pattern_2 = tok.decode(opens_1, highs_1, lows_1, closes_1, pat1m)
        
            tok.apply_results(case, pattern_2)

            # if i_5 != -1:
            #     closes_5 = sv.data_5[i_5-sv.settings.chunk_len*2:i_5, 4]
            #     highs_5 = sv.data_5[i_5-sv.settings.chunk_len*2:i_5, 2]
            #     lows_5 = sv.data_5[i_5-sv.settings.chunk_len*2:i_5, 3]
            #     opens_5 = sv.data_5[i_5-sv.settings.chunk_len*2:i_5, 1]

            #     case = tok.check_pattern(sv.data_5[i_5][1], sv.data_5[i_5][2], sv.data_5[i_5][3], sv.data_5[i_5][4], 0.004, 0.01)
            #     if case == 'none':
            #         i_1+=1
            #         continue
            #     pat1m = 'long' if closes_1[-1]>opens_1[-1] else 'short'
            #     pattern_2 = tok.decode(opens_5, highs_5, lows_5, closes_5, pat1m)
            
            #     tok.apply_results(case, pattern_2)
            i_1+=1
    print('=================================================')
    print(sv.token_model_up)
    print('=================================================')
    print(sv.token_model_down)