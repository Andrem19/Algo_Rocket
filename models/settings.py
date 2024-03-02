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