from datetime import datetime

class Settings:
    def __init__(self):
        self.target_len: int = 5
        self.init_stop_loss: float = 0.008
        self.take_profit: float = 0.20

        self.main_variant: int = 1
        self.printer: bool = False
        self.drawing: bool = False
        self.send_pic: bool = False
        self.pic_collections: bool = False
        self.iter_count: int = 1
        self.time = 5
        self.coin: str = 'BTCUSDT'
        self.amount: int = 20
        self.chunk_len: int = 30
        self.only: int = 0
        self.s = [1,2]
        self.counter: int = 0

        self.start_date = datetime(2017, 1, 1)
        self.finish_date = datetime(2024, 1, 1)

        self.taker_fee: float = 0.12
        self.maker_fee: float = 0.12

        self.hot_count_on_off: int = 1
        self.cold_count_on_off: int = 0
        self.cold_count_iterations: int = 1000
        self.cold_count_print_all = 1
        self.cold_count_print_res = {
                                        'final': 0,
                                        'ham_1a': 0,
                                        'ham_1b': 0,
                                        'rsi_1': 0,
                                        'down_1': 0,
                                        'ham_5a': 0,
                                        'ham_5aa': 0,
                                        'ham_5b': 0,
                                        'ham_5bb': 0,
                                        'rsi_5': 0,
                                        'coint_15': 0,
                                        'adx_5': 0,
                                        'ham_15': 0,
                                        'mid_5': 0,
                                        'mid_15': 0,
                                        'test_5': 0,
                                    }