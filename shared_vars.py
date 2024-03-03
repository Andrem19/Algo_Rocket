import numpy as np
import setup as set
from models.signal import Signal
from models.increaser import Increaser, GeneralIncreaser
from models.settings import Settings
from datetime import datetime, timedelta

days_gap = {}
telegram_api = 'API_TOKEN_1'

signal: Signal = Signal()
counter = 0
unique_ident = None
time_start = 0
time_finish = 0

data: np.ndarray = None
data_1: np.ndarray = None
data_2: np.ndarray = None
data_5: np.ndarray = None
data_15: np.ndarray = None
data_30: np.ndarray = None

settings: Settings = set.setup()

dropdowns_accumulate = {}
percent_accumulate = []
max_border_accum = []
min_border_accum = []
sum_saldo = []

gen_increaser = GeneralIncreaser()
candel_dict_5 = {}
candle_dict_15 = {}
candel_dict_1 = {}
candel_dict_2 = {}