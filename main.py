import shared_vars as sv
import coins as coins
from datetime import datetime
import setup as setup
import helpers.util as util
from itertools import product
import random
import variant.single_saldo as ss
import variant.multi_saldo as ms
from datetime import timedelta
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
        pass
    
    sv.time_finish = datetime.now().timestamp()
    seconds = sv.time_finish-sv.time_start
    tm = str(timedelta(seconds=seconds))
    print(f'uid: {sv.unique_ident}')
    print(f'Exec speed: {tm}')


if __name__ == "__main__":
    setup.setup()
    asyncio.run(main(sys.argv[1:]))