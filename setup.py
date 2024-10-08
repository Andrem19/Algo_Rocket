from models.settings import Settings
import shared_vars as sv
from datetime import datetime

def setup():
    settings = Settings()
    settings.target_len = 2
    settings.init_stop_loss = 0.01
    settings.take_profit = 0.20

    settings.main_variant = 2
    settings.printer = False
    settings.drawing = False
    settings.send_pic = False
    settings.pic_collections = False
    settings.iter_count = 1
    settings.time = 60
    settings.coin = 'BTCUSDT'
    settings.amount = 20
    settings.chunk_len = 30
    settings.only = 0
    settings.s = [1] if settings.only == 1 else [2] if settings.only == 2 else (1,2)
    settings.counter = 0

    settings.start_date = datetime(2017, 1, 1)
    settings.finish_date = datetime(2024, 5, 1)

    settings.taker_fee = 0.2
    settings.maker_fee = 0.2

    settings.curren_uid = '4a7240f0'
    settings.hot_count_on_off = 1
    settings.cold_count_on_off = 0
    settings.cold_count_iterations = 100
    settings.cold_count_print_all = 1
    settings.cold_count_print_res = {
                                    'final': 0,
                                    'stub': 0,
                                    'ham_1a': 0,
                                    'ham_1aX': 0,
                                    'ham_1b': 0,
                                    'rsi_1': 0,
                                    'ham_1bx': 0,
                                    'ham_1by': 0,
                                    'ham_1bz': 0,
                                    'ham_2a': 0,
                                    'ham_2b': 0,
                                    'down_1': 0,
                                    'down_15': 0,
                                    'ham_5a': 0,
                                    'ham_5aX': 0,
                                    'ham_5aa': 0,
                                    'ham_5b': 0,
                                    'ham_5bX': 0,
                                    'ham_5bb': 0,
                                    'lst_5': 0,
                                    'rsi_5': 0,
                                    'coint_15': 0,
                                    'adx_5': 0,
                                    'adx_5aa': 0,
                                    'ham_15': 0,
                                    'mid_1': 0,
                                    'mid_15': 0,
                                    'test_5': 0,
                                    'test_10': 0,
                                }
    sv.settings = settings
    return settings