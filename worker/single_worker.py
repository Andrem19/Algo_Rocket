import worker.single_proccess as prc
import signal as sg
import shared_vars as sv
import worker.single_signal as sg
import traceback


def run(data, last_position, is_first_iter: bool):
    try:
        chunk_len = sv.settings.chunk_len
        data_len = len(data)
        data_len_for_loop = data_len - chunk_len*3
        profit_list: list = []
        if last_position:
            profit_list.append(last_position)


        i = chunk_len*3+1

        while i < data_len_for_loop:
            sg.get_signal(i, data)

            if sv.signal.signal in sv.settings.s:

                tm1 = prc.position_proccess(i, profit_list, data, is_first_iter)

                i+=tm1
            else: 
                i+=1

        if is_first_iter == False:
            del profit_list[0]
        return profit_list
    except Exception as e:
        print(f'Error [run] {e}')
        print(traceback.format_exc())