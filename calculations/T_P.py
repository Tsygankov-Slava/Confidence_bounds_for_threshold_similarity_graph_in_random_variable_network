import numpy as np
from Data import Data
from auxiliary.frange import frange


# Статистика Пирсона
class T_P(Data):
  def __init__(self, path_to_csv, x_points):
    super().__init__(path_to_csv = path_to_csv)

    self.x_points = x_points

    self.T = {}
    self.size_T = self.shares_number

    self.R = [] # Ковариационная матрица из кореляций Пирсона
    self.get_selective_covariance_matrix_R()
    self.calc_T_P()

  # Функция для расчета корреляции rij
  def calc_rij(self, i, j):
    Xi = self.stocks_profitability[i]
    Xj = self.stocks_profitability[j]

    return np.corrcoef(Xi, Xj)[0, 1]

  # Функция для вычисления матрицы ковариации
  def get_selective_covariance_matrix_R(self):
    for i in range(self.shares_number):
      line = []
      for j in range(self.shares_number):
        rij = self.calc_rij(i, j)
        line.append(rij)
      self.R.append(line)

  # Функция для вычисления Tij (Корреляция Пирсона)
  def calc_Tij_P(self, i, j, gamma_0):
    Tij = 0
    if i != j:
      numerator = np.sqrt(self.observations_number - 2) / 2
      log_term_1 = (1 + self.R[i][j]) / (1 - self.R[i][j])
      log_term_2 = (1 + gamma_0) / (1 - gamma_0)

      Tij = numerator * (np.log(log_term_1) - np.log(log_term_2))
    return Tij

  # Функция для получения матрицы Tij_P (Корреляция Пирсона)
  def calc_T_P(self):
    for gamma_0 in self.x_points:
      if gamma_0 not in self.T:
        self.T[gamma_0] = []
      for i in range(self.size_T):
        line= []
        for j in range(self.size_T):
          line.append(self.calc_Tij_P(i, j, gamma_0))
        self.T[gamma_0].append(line)