import numpy as np
import setup as set
from models.signal import Signal
from models.increaser import Increaser, GeneralIncreaser
from models.settings import Settings
from datetime import datetime, timedelta
from models.reactor import Reactor
from commander.com import Commander
from models.cur_pos import Position

days_gap = {}
telegram_api = 'API_TOKEN_1'

signal: Signal = Signal()
counter = 0
unique_ident = None
time_start = 0
time_finish = 0

preload_sets = {}
preload = False
reactor: Reactor = None
position: Position = None
all_positions = None

data: np.ndarray = None
data_1: np.ndarray = None
data_2: np.ndarray = None
data_5: np.ndarray = None
data_15: np.ndarray = None
data_30: np.ndarray = None
data_60: np.ndarray = None

settings: Settings = set.setup()

dropdowns_accumulate = {}
percent_accumulate = []
max_border_accum = []
min_border_accum = []
sum_saldo = []

gen_increaser = GeneralIncreaser()
candel_dict_5 = {}
candle_dict_15 = {}
candle_dict_60 = {}
candel_dict_1 = {}
candel_dict_2 = {}

max_val = {
        'ham_1a': 0,
        'ham_1b': 0,
        'ham_5a': 0,
        'ham_1aX': 0,
        'ham_5aX': 0,
        'ham_5b': 0,
        'ham_5bX': 0,
        'ham_15': 0,
        'down_1': 0,
        'rsi_1': 0,
        'rsi_5': 0,
        'rsi_15': 0,
        'adx_5': 0,
        'dir_5': 0,
    }

frozen = 0
adx_counter = 0

global_trend = 'none'
close_60 = []

list_of_patterns = []

ath = {}

token_model_up = {
    'high<>body*0.6': {
        'less': 0,
        'bigger': 0,
    },
    'low<>body*0.6': {
        'less': 0,
        'bigger': 0,
    },
    'cndl_not_less': {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
    },
    'glob1htrend15': {
        'up': 0,
        'down': 0,
        'none': 0
    },
    'close>prevLow': {
        True: 0,
        False: 0,
    },
    'close<prevHigh': {
        True: 0,
        False: 0,
    },
    'last1m': {
        'long': 0,
        'short': 0,
    },
    'rsi': {
        '>70': 0,
        '<30': 0,
        '<70>30': 0,
    },
    'rise2mult3': {
        'less': 0,
        'bigger': 0,
    },
    'all_True_any_False_3': {
        'allDown': 0,
        'allUp': 0,
        'none': 0
    },
}
token_model_down = {
    'high<>body*0.6': {
        'less': 0,
        'bigger': 0,
    },
    'low<>body*0.6': {
        'less': 0,
        'bigger': 0,
    },
    'cndl_not_less': {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
    },
    'glob1htrend15': {
        'up': 0,
        'down': 0,
        'none': 0
    },
    'close>prevLow': {
        True: 0,
        False: 0,
    },
    'close<prevHigh': {
        True: 0,
        False: 0,
    },
    'last1m': {
        'long': 0,
        'short': 0,
    },
    'rsi': {
        '>70': 0,
        '<30': 0,
        '<70>30': 0,
    },
    'rise2mult3': {
        'less': 0,
        'bigger': 0,
    },
    'all_True_any_False_3': {
        'allDown': 0,
        'allUp': 0,
        'none': 0
    },
}
saldo_sum = 0

commander: Commander = None
last_command = ''

rsi_5_couner = 40
is_success = False

ham_1b_stls = []

ham_1b_triger = 0
price_close = 0
frozen = 0
delay = 0
volume = 0