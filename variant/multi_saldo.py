import shared_vars as sv
import os
import helpers.tel as tel
import helpers.get_data as gd
import helpers.util as util
import helpers.statistic_count as stat
import random
import time
import copy
import numpy as np
import traceback
import coins
import multiprocessing
from datetime import datetime
import worker.multi_worker as w
import concurrent.futures
import helpers.vizualizer as viz
import helpers.print_info as printer
import helpers.statistic_count as stat

output_lock = multiprocessing.Lock()

async def process_result(result, coin, coin_list_len):
    if result:
        report = stat.proceed_positions(result)
        report['coin'] = coin
        report = util.insert(report, 'Num', coin_list_len, 0)
        printer.print_colored_dict(report)
        if sv.settings.send_pic:
            pt = util.get_points_value(len(result))
            drpd, tp_cl = stat.dangerous_moments(result)
            with output_lock:
                path = viz.plot_time_series(result, True, pt, True, drpd, {})
                await tel.send_inform_message(f'{coin}', path, True)

def do_job(coin: str, profit_path: str, lock):
    try:

        sv.ath[coin] = 0
        file_coin = f'_crypto_data/{coin}/{coin}_1m.csv'
        if not os.path.exists(file_coin):
            print(f'{coin} doesnt exist')
            return None
        
        #==============15m cointegration=================
        sv.settings.coin = coin
        data_1 = gd.load_data_sets(15)
        sv.settings.coin = 'BTCUSDT'
        data_2 = gd.load_data_sets(15)
        min_time = max(np.min(data_1[:, 0]), np.min(data_2[:, 0]))
        max_time = min(np.max(data_1[:, 0]), np.max(data_2[:, 0]))
        data_1 = data_1[(data_1[:, 0] >= min_time) & (data_1[:, 0] <= max_time)]
        data_2 = data_2[(data_2[:, 0] >= min_time) & (data_2[:, 0] <= max_time)]
        sv.data_1 = data_1[np.argsort(data_1[:, 0])]
        sv.data_2 = data_2[np.argsort(data_2[:, 0])]
        sv.candel_dict_1 = util.create_candle_dict(sv.data_1)
        sv.candel_dict_2 = util.create_candle_dict(sv.data_2)
        #=======================================================
        sv.settings.coin = coin

        data_gen_1m = gd.load_data_in_chunks(sv.settings, 100000, 1)
        sv.data_5 = gd.load_data_sets(5)
        sv.candel_dict_5 = util.create_candle_dict(sv.data_5)
        #==============1h================================
        # sv.data_60 = gd.load_data_sets(60)
        # sv.candle_dict_60 = util.create_candle_dict(sv.data_60)
        #================================================
        
        position_collector = []
        last_position = {}
        is_first_iter = True
        
        for data in data_gen_1m:
            # print(f'data len {len(data)} {coin}')
            sv.signal.signal = 3
            profit_list = w.run(data, last_position, is_first_iter)

            if len(profit_list) > 0:
                is_first_iter = False
                last_position = profit_list[-1]
                with lock:
                    util.save_list(profit_list, profit_path)
                    position_collector.extend(profit_list)
                    if sv.settings.pic_collections:
                        list_of_lists = data.tolist()
                        viz.draw_candlesticks_positions(list_of_lists, profit_list, f'{sv.settings.coin}-{datetime.fromtimestamp(float(data[0][0])/1000)}-{datetime.fromtimestamp(float(data[-1][0])/1000)}')
            elif len(profit_list) == 0:
                is_first_iter = True

        return position_collector
    except Exception as e:
        print(f'Error [do_job] {e}')
        print(traceback.format_exc())

def unpack_and_call(args):
    return do_job(*args, output_lock)

async def mp_saldo(coin_list, use_multiprocessing=True):
    random.shuffle(coin_list)
    coin_list_len = len(coin_list)
    util.start_of_program_preparing()
    profit_path = f'_profits/{sv.unique_ident}_profits.txt'
    if use_multiprocessing:
        Executor = concurrent.futures.ProcessPoolExecutor
        with Executor(max_workers=4) as executor:
            for coin, result in zip(coin_list, executor.map(unpack_and_call, [(coin, profit_path) for coin in coin_list])):
                await process_result(result, coin, coin_list_len)
                coin_list_len-=1
    else:
        for coin in coin_list:
            result = unpack_and_call((coin, profit_path))
            await process_result(result, coin, coin_list_len)


    all_positions = util.load_positions('_profits')
    if len(all_positions)>0:
        filtred_positions = stat.filter_positions(all_positions)
        dropdowns, type_collection = stat.dangerous_moments(filtred_positions)
        med_dur = stat.calc_med_duration(filtred_positions)
        stat_dict = stat.get_type_statistic(filtred_positions)
        full_report = stat.proceed_positions(filtred_positions)
        full_report['med_dur'] = med_dur
        full_report['coin'] = 'All contracts'
        print(f'\033[0;31mGeneral report:\033[0m')
        print(full_report)
        print(f'\033[0;31mDropdowns:\033[0m')
        print(dropdowns)
        print('\033[0;31mStatistic types:\033[0m')
        print(stat_dict)
        print('\033[0;31mDays gap:\033[0m')
        print(sv.days_gap)
        print(type_collection)
        print(sv.max_val)
        dict_splited = stat.sort_by_type(copy.deepcopy(filtred_positions))
        for key, pos in dict_splited.items():
            if sv.settings.cold_count_print_all or sv.settings.cold_count_print_res[key] ==1:
                drdw, type_collection = stat.dangerous_moments(pos)
                points = util.get_points_value(len(pos))
                path = viz.plot_time_series(pos, True, points, True, drdw, {})
                await tel.send_inform_message(f'{key}', path, True)
                time.sleep(0.5)

        points = util.get_points_value(len(filtred_positions))
        path = viz.plot_time_series(filtred_positions, True, points, True, dropdowns, {})
        await tel.send_inform_message(f'{full_report}', path, True)