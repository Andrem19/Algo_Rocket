import worker.multi_proccess as prc
import helpers.util as util
import shared_vars as sv
import worker.multi_signal as sg
# import worker.multi_signal_2 as sg_2
import copy
from models.settings import Settings
import traceback
from models.signal import Signal


def run(data, last_position, is_first_iter: bool):
    try:
        chunk_len = sv.settings.chunk_len
        data_len = len(data)
        data_len_for_loop = data_len - max(3*15, 5*5)+1
        profit_list: list = []

        if last_position:
            profit_list.append(last_position)

        i_1 = sv.settings.chunk_len*2*5+1 if is_first_iter else sv.settings.chunk_len*7

        while i_1 < data_len_for_loop:
            i_5 = util.get_candel_index(data[i_1][0], sv.candel_dict_5)
            i_15_1 = util.get_candel_index(data[i_1][0], sv.candel_dict_1)
            i_15_2 = util.get_candel_index(data[i_1][0], sv.candel_dict_2)
            # i_15_3 = util.get_candel_index(data[i_1][0], sv.candle_dict_60)

            sg.get_signal(i_1, i_5, i_15_1, i_15_2, data, sv.settings)

            if sv.signal.signal in sv.settings.s:
                # if sv.signal.signal == 1 and sv.global_trend in ['none', 'down']:
                #     i_1+=1
                #     continue
                # if sv.signal.signal == 2 and sv.global_trend in ['none', 'up']:
                #     i_1+=1
                #     continue


                tm = prc.position_proccess(profit_list, data, is_first_iter)

                if profit_list[-1]['profit']<0:
                    if sv.gen_increaser.increase_border > 0:
                        sv.gen_increaser.increase_border = 12

                i_1+=tm
            else: 
                i_1+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())