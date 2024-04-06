import os
import pandas as pd
import talib
import coins_2 as coin_2

# Создаем пустой DataFrame для хранения RSI
rsi_df = None

# Проходим по всем файлам в папке
for coin in coin_2.best_set:
    data_folder = f'_crypto_data/{coin}'
    for file in os.listdir(data_folder):
        if file.endswith('_1m.csv'):
            # Читаем данные из файла
            df = pd.read_csv(os.path.join(data_folder, file), header=None)
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            
            # Вычисляем RSI
            rsi = talib.RSI(df['close'], timeperiod=16)
            
            # Создаем новый DataFrame для RSI этой монеты
            rsi_coin_df = pd.DataFrame({
                'timestamp': df['timestamp'],
                file[:-7]: rsi
            })
            
            # Если это первая монета, то просто сохраняем DataFrame
            if rsi_df is None:
                rsi_df = rsi_coin_df
            else:
                # Иначе объединяем с уже существующим DataFrame по timestamp
                rsi_df = pd.merge(rsi_df, rsi_coin_df, on='timestamp', how='outer')

# Заполняем пропущенные значения нулями
rsi_df.fillna(0, inplace=True)

# Сохраняем RSI в файл
rsi_df.to_csv('rsi_data.csv', index=False)
