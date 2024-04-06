import helpers.tel as tel
from decouple import config
from telegram import Bot
import asyncio
import coins
import coins_2
import pandas as pd

# Читаем только первые 1000 строк
df = pd.read_csv('rsi_data.csv', nrows=1000)

# Печатаем DataFrame
print(df)


# seen = set()
# duplicates = set()
# print(f'Lenth: {len(coins_2.all_coins)}')
# for item in coins_2.all_coins:
#     if item in seen:
#         duplicates.add(item)
#     seen.add(item)

# if duplicates:
#     print(f"Duplicate elements found: {duplicates}")
# else:
#     print("No duplicates found")
# hyper_liquid_set = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'FTMUSDT', 'DOGEUSDT', 'OPUSDT', 'RUNEUSDT', 'NEARUSDT', 'SEIUSDT', 'APTUSDT', 'ARBUSDT', 'MKRUSDT', 'AVAXUSDT', 'MATICUSDT', 'FILUSDT', 'TIAUSDT', 'LDOUSDT', 'ORDIUSDT', 'INJUSDT', 'SUIUSDT', 'LINKUSDT', 'SNXUSDT', 'XRPUSDT', 'STXUSDT', 'ADAUSDT', 'KBONKUSDT', 'RNDRUSDT', 'PENDLEUSDT', 'BNBUSDT', 'WLDUSDT', 'FETUSDT', 'DYDXUSDT', 'TONUSDT', 'BLURUSDT', 'CFXUSDT', 'FXSUSDT', 'ATOMUSDT', 'AAVEUSDT', 'BCHUSDT', 'LTCUSDT', 'APEUSDT', 'UNIUSDT', 'BADGERUSDT', 'DOTUSDT', 'IMXUSDT', 'JTOUSDT', 'GALAUSDT', 'CRVUSDT', 'POLYXUSDT', 'NTRNUSDT', 'CYBERUSDT', 'TRBUSDT', 'BSVUSDT', 'BNTUSDT', 'FTTUSDT', 'NEOUSDT', 'MINAUSDT', 'ACEUSDT', 'BLZUSDT', 'COMPUSDT', 'ARKUSDT', 'OGNUSDT', 'TRXUSDT', 'RSRUSDT', 'RDNTUSDT', 'BIGTIMEUSDT', 'USTCUSDT', 'YGGUSDT', 'STGUSDT', 'GMTUSDT', 'MAVUSDT', 'GMXUSDT', 'KLUNCUSDT', 'ORBSUSDT', 'CANTOUSDT', 'KASUSDT', 'ILVUSDT', 'GASUSDT', 'LOOMUSDT', 'SUPERUSDT', 'ZENUSDT', 'REQUSDT', 'OXUSDT', 'RLBUSDT', 'UNIBOTUSDT', 'BANANAUSDT', 'WIFUSDT', 'ONDOUSDT', 'PIXELUSDT', 'AIUSDT', 'BOMEUSDT', 'ZETAUSDT', 'ETCUSDT', 'JUPUSDT', 'STRKUSDT', 'ALTUSDT', 'PYTHUSDT', 'TAOUSDT', 'ENSUSDT', 'MEMEUSDT', 'MANTAUSDT', 'SUSHIUSDT', 'DYMUSDT', 'XAIUSDT', 'MAVIAUSDT', 'CAKEUSDT', 'UMAUSDT', 'PEOPLEUSDT', 'PANDORAUSDT']

# num = 0
# my_set = coins.all_coins
# my_set.extend(coins.new_coins)
# print(f'All my coins: {len(my_set)}')
# print(f'Hyperliquid coins: {len(hyper_liquid_set)}')
# for cn in hyper_liquid_set:
#     if cn in my_set:
#         num+=1
#         print(num, cn)