import shared_vars as sv
import coins as coins
from datetime import datetime
import setup as setup
import helpers.util as util
import variant.pattern_sarcher as ps
from itertools import product
import random
import variant.single_saldo as ss
import variant.multi_saldo as ms
from datetime import timedelta
import helpers.tools as tools
from models.reactor import Reactor, MethodFunc
from models.settings import Settings
import cold_count as cc
import asyncio
import high_koff as hk
import io
import time as tm
import sys
import uuid
import helpers.tel as tel

sv.telegram_api = 'API_TOKEN_1'
coin_list = coins.best_set # coins.new_collection + coins.coins_to_add#['LTCUSDT']# coins.all_coins

async def main(args):
    
    sv.time_start = datetime.now().timestamp()
    global coin_list
    sv.unique_ident = str(uuid.uuid4())[:8]
    print(f'uid: {sv.unique_ident}')
    if sv.settings.main_variant == 1:
        await ss.mp_saldo(coin_list, True)
    elif sv.settings.main_variant == 2:
        if sv.settings.hot_count_on_off==1:
            await ms.mp_saldo(coin_list)
        if sv.settings.cold_count_on_off==1:
            if sv.settings.hot_count_on_off==0:
                sv.unique_ident = sv.settings.curren_uid
            await cc.count_run()
    elif sv.settings.main_variant == 3:
        #Search patterns
        await ps.search_pattern(coin_list)
    elif sv.settings.main_variant == 4:
        for _ in range(1000):
            sv.unique_ident = str(uuid.uuid4())[:8]

            min_br = random.randint(30, 60)
            max_br = min_br + random.randint(10, 40)
            method_1 = MethodFunc(tools.check_rsi, ['closes', 27, min_br, max_br])
            
            first_can = random.choice(['highs1', 'opens1'])
            sec_can = 'lows1' if first_can == 'highs1' else 'closes1'
            ch = [0.016, 0.026, 0.036] if first_can == 'highs1' else [0.006, 0.016, 0.024]
            method_2 = MethodFunc(tools.check_high_candel, [first_can, sec_can, random.choice(ch)])

            method_3 = MethodFunc(tools.all_True_any_False, ['closes', 'opens', random.choice([2, 3, 4]), random.choice(['all', 'any']), random.choice([True, False])])
            
            opcl = random.choice(['lower', 'bigger', 'none'])
            method_4 = MethodFunc(tools.open_close, ['opens1', 'closes1', opcl])
            
            method_5 = MethodFunc(tools.low_high_tails, ['opens1', 'highs1', 'lows1', 'closes1', random.choice(['low', 'high', 'none']), random.choice(['lower', 'bigger']), random.choice([0.4, 0.8, 1.2, 2])])

            chs = ['lowest', 'highest', 'none']
            method_6 = MethodFunc(tools.last_lowest_highest, ['highs', 'lows', random.choice(chs), random.choice([10, 20, 30])])
            
            method_7 = MethodFunc(tools.last_close_higher, ['highs', 'lows', 'closes', random.choice(['lower', 'higher', 'none']), random.choice(['low', 'high'])])
            

            methods = [method_1, method_2, method_3, method_4, method_5, method_6, method_7]
            selected_methods = [method_1, method_2]
            additional_methods = random.sample(methods[2:], random.randint(2, 4))
            selected_methods.extend(additional_methods)
            reactor = Reactor(selected_methods, 1)
            reactor.print_pattern()
            sv.reactor = reactor

            await ss.mp_saldo(coin_list, False)

    
    sv.time_finish = datetime.now().timestamp()
    seconds = sv.time_finish-sv.time_start
    tm = str(timedelta(seconds=seconds))
    print(f'uid: {sv.unique_ident}')
    print(f'Exec speed: {tm}')


if __name__ == "__main__":
    setup.setup()
    asyncio.run(main(sys.argv[1:]))