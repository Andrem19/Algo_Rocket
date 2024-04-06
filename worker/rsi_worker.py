import worker.single_proccess as prc
import helpers.util as util
import shared_vars as sv
import worker.single_signal as sg
# import worker.multi_signal_2 as sg_2
import copy
from models.settings import Settings
import traceback
from models.signal import Signal


def run(data, timestamp, profit_list, first_iter):
    try:
        i_1 = util.get_candel_index(timestamp, sv.candel_dict_1)+1
        sg.get_signal(i_1, data)

        if sv.signal.signal in sv.settings.s:
            tm = prc.position_proccess(i_1, profit_list, data, first_iter)
            return profit_list
        return None
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())