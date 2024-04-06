import pandas as pd
import coins_2 as coins_2
import shared_vars as sv
import helpers.get_data as gd
import helpers.util as util
import worker.rsi_worker as w
from datetime import datetime


coefficient = 0.3
def iterator_worker(chunksize=50000):

    for coin in coins_2.best_set:
        sv.settings.coin = coin
        sv.data_1 = gd.load_data_sets(1)
        sv.candel_dict_1 = util.create_candle_dict(sv.data_1)
        chunk_iterator = pd.read_csv('rsi_data.csv', chunksize=chunksize)
        profit_list = []
        first_iter = True
        for chunk in chunk_iterator:
            # Проходим по каждой минуте в текущем блоке
            for index, row in chunk.iterrows():
                # Исключаем монеты, у которых RSI равно 0
                row_filtered = row[row != 0.0]

                # Если осталось меньше 10 столбцов, пропускаем эту итерацию
                if len(row_filtered) < 40 or coin not in row_filtered:
                    continue
                # pd.set_option('display.float_format', '{:.2f}'.format)
                # print(row_filtered)
                # Вычисляем средний RSI
                mean_rsi = row_filtered.drop('timestamp').mean()

                # if row_filtered[coin] > mean_rsi * (1 + coefficient):
                if row_filtered[coin] < 19 and mean_rsi > 30:
                    result = w.run(sv.data_1, row["timestamp"], profit_list, first_iter)
                    if result is not None:
                        print(f'В {index} (timestamp: {row["timestamp"]}) монета {coin} имеет RSI {row_filtered[coin]}, что меньше среднего {mean_rsi} на {coefficient * 100}%')
                        first_iter = False
                        print(result[-1])

