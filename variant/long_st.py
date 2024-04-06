import random
import helpers.util as util
import shared_vars as sv
import helpers.get_data as gd
import worker.long_str_worker as w

async def lg_saldo(coin_list, use_multiprocessing=False):
    random.shuffle(coin_list)
    coin_list_len = len(coin_list)
    util.start_of_program_preparing()
    profit_path = f'_profits/{sv.unique_ident}_profits.txt'

    for coin in coin_list:
        sv.settings.coin = coin
        data = gd.load_data_sets(sv.settings.time)

        sv.signal.signal = 3
        profit_list = w.run(data)