import os

import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt


class Data:
  P = 0.9

  def __init__(self, path_to_csv):
    self.country = path_to_csv.split('/')[1]

    self.data = pd.read_csv(path_to_csv).drop(columns=['Date'])
    self.shares_number = self.data.shape[1] # Кол-во акций
    self.M = self.shares_number * (self.shares_number - 1) // 2 # Кол-во пар акций
    print(f"Кол-во пар акций: {self.M}")
    self.stocks_profitability = [] # Доходности для каждой акции (Цена закрытия)
    self.get_stocks_profitability()
    self.plot_and_save_profitability()

    self.c_ij_e = self.calc_c_ij_e()
    self.c_ij_n = self.calc_c_ij_n()

    self.observations_number = len(self.stocks_profitability[0]) # Кол-во наблюдений

  # Функция для получения доходности акций
  def get_stocks_profitability(self):
      for ticker in self.data:
          stock_profitability = []
          close_prices = self.data[ticker]
          for i in range(1, len(close_prices)):
              prev_price = close_prices.iloc[i-1]
              curr_price = close_prices.iloc[i]

              profitability = np.log(curr_price / prev_price)
              stock_profitability.append(profitability)

          self.stocks_profitability.append(stock_profitability)

  def plot_and_save_profitability(self):
      os.makedirs('Data_For_Article/Graphics/Profitability/', exist_ok=True)
      filename = f'Data_For_Article/Graphics/Profitability/{self.country}_Profitability.png'
      for ticker, stock_profitability in zip(self.data.keys(), self.stocks_profitability):
          plt.plot(stock_profitability, label=ticker)

      plt.title(f'Stock returns for {self.country}')
      plt.xlabel('Time index')
      plt.ylabel('Profitability')
      plt.legend()
      plt.grid()
      plt.savefig(filename, format='png')
      plt.close()

  # Функция для расчета c_ij_e
  def calc_c_ij_e(self):
      probability = (1 - self.P) / self.M
      return stats.norm.ppf(probability)

  # Функция для расчета c_ij_n
  def calc_c_ij_n(self):
      probability = (1 - self.P) / self.M
      return stats.norm.ppf(1 - probability)