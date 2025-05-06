import os
import yfinance as yf
from matplotlib import pyplot as plt

from data_loading.Argentina.tickers import merval_tickers
from data_loading.Australia.tickers import asx50_tickers
from data_loading.Brazil.tickers import ibov_tickers
from data_loading.Canada.tickers import tsx_tickers
from data_loading.China.tickers import hang_seng_tickers
from data_loading.India.tickers import nifty_tickers
from data_loading.Italy.tickers import ftse_mib_tickers
from data_loading.Japan.tickers import nikkei_225_tickers
from data_loading.Spain.tickers import ibex_35_tickers
from data_loading.Sweden.tickers import omx_stockholm_30_tickers
from data_loading.UK.tickers import ftse_100_tickers
from data_loading.USA.tickers import djia_tickers

tickers_to_csv_list = [
    (merval_tickers,           "Argentina/Argentina_daily_close_prices_2023.csv"),
    (asx50_tickers,            "Australia/Australia_daily_close_prices_2023.csv"),
    (ibov_tickers,             "Brazil/Brazil_daily_close_prices_2023.csv"),
    (tsx_tickers,              "Canada/Canada_daily_close_prices_2023.csv"),
    (hang_seng_tickers,        "China/China_daily_close_prices_2023.csv"),
    (nifty_tickers,            "India/India_daily_close_prices_2023.csv"),
    (ftse_mib_tickers,         "Italy/Italy_daily_close_prices_2023.csv"),
    (nikkei_225_tickers,       "Japan/Japan_daily_close_prices_2023.csv"),
    (ibex_35_tickers,          "Spain/Spain_daily_close_prices_2023.csv"),
    (omx_stockholm_30_tickers, "Sweden/Sweden_daily_close_prices_2023.csv"),
    (ftse_100_tickers,         "UK/UK_daily_close_prices_2023.csv"),
    (djia_tickers,             "USA/USA_daily_close_prices_2023.csv"),
]

colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

START_DATA_FOR_ANALYSIS = '2023-01-01'
END_DATA_FOR_ANALYSIS   = '2023-12-31'

for tickers_to_csv in tickers_to_csv_list:
    tickers = tickers_to_csv[0]
    csv_file_name = tickers_to_csv[1]

    data = yf.download(tickers, start=START_DATA_FOR_ANALYSIS, end=END_DATA_FOR_ANALYSIS) # Скачиваем данные для акций из tickers за 2023 год
    daily_data_close_original =  data['Close'] # Используем данные по закрытию цен
    daily_data_close_original.to_csv(f"{csv_file_name[:-4]}_original.csv")

    daily_data_close = daily_data_close_original.apply(lambda x: x.interpolate(method='linear')).round(4)
    daily_data_close = daily_data_close.bfill()
    daily_data_close = daily_data_close.ffill()

    daily_data_close.to_csv(csv_file_name)

    for name in daily_data_close:
        print(f"{name} : {daily_data_close[name].max()}")

    # Строим графики по ценам закрытия и сохраняем в "Data_For_Article/Closing_Prices_Graphics/"
    plt.figure(figsize=(10, 5))

    for i, name in enumerate(daily_data_close.columns):
        daily_data_close[name].plot(title=f'Closing Prices for {csv_file_name.split("/")[0]} 2023',
                                     color=colors[i % len(colors)], label=name)

        last_value = daily_data_close[name].iloc[-1]
        plt.text(daily_data_close.index[-1], last_value, name, color=colors[i % len(colors)],
                 fontsize=9, verticalalignment='bottom', horizontalalignment='right')

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.legend(loc='upper left')

    os.makedirs('../Data_For_Article/Closing_Prices_Graphics/', exist_ok=True)

    plt.savefig(f"../Data_For_Article/Closing_Prices_Graphics/{csv_file_name.split('/')[0]}_closing_prices.png", format='png')
    plt.show(block=False)
    plt.close()
