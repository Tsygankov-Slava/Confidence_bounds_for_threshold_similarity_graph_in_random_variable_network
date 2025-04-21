from typing import Any

from scipy.stats import kendalltau
import numpy as np
from Data import Data


class Data_:
    def __init__(self, value=0, left_link=0, right_link=0):
        self.left_link = left_link
        self.right_link = right_link
        self.value = value

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.arr = []
        self.arr_size = 0

# Статистика Кенделла
class T_Kd(Data):
    Pcc = []

    def __init__(self, path_to_csv, x_points):
        super().__init__(path_to_csv = path_to_csv)

        self.x_points = x_points

        self.T = {}
        self.size_T = self.shares_number

        self.G = []
        self.get_selective_covariance_matrix_G()
        self.calc_T_Kd()

    def calc_I_ij_Kd(self, i, j, t, s):
        Xi = self.stocks_profitability[i]
        Xj = self.stocks_profitability[j]

        left = Xi[t] - Xi[s]
        right = Xj[t] - Xj[s]

        if left * right >= 0:
            return 1
        else:
            return -1

    def calc_gamma_ij_Kd(self, i, j):
        Xi = self.stocks_profitability[i]
        Xj = self.stocks_profitability[j]

        kendall_corr, _ = kendalltau(Xi, Xj)
        return kendall_corr

    def get_selective_covariance_matrix_G(self):
        size = self.shares_number
        for i in range(size):
            line = []
            for j in range(size):
                gamma_ij = self.calc_gamma_ij_Kd(i, j)
                line.append(gamma_ij)
            self.G.append(line)

    def calc_Pc(self, i, j):
        return (self.G[i][j] + 1) / 2

    def calc_Pcc(self, i, j):
        def merge(arr_l, arr_r):
            arr_size = len(arr_l) + len(arr_r)
            arr = [Data_() for _ in range(arr_size)]
            l, r = 0, 0

            for i in range(arr_size):
                arr[i].left_link = l
                arr[i].right_link = r
                if (l < len(arr_l) and r < len(arr_r) and arr_l[l].value <= arr_r[r].value) or r == len(arr_r):
                    arr[i].value = arr_l[l].value
                    l += 1
                else:
                    arr[i].value = arr_r[r].value
                    r += 1

            return arr

        def initialize(node):
            node.left = None
            node.right = None
            node.arr = []
            node.arr_size = 0

        def add(node, tl, tr, arr):
            if tr - tl == 1:
                node.arr = [Data_(arr[tl])]
                node.arr_size = 1
                return

            tc = (tl + tr) // 2
            node.left = Node()
            initialize(node.left)
            add(node.left, tl, tc, arr)

            node.right = Node()
            initialize(node.right)
            add(node.right, tc, tr, arr)

            node.arr = merge(node.left.arr, node.right.arr)
            node.arr_size = len(node.arr)

        def count(node, tl, tr, l, r, p):
            if tl == l and tr == r:
                return r - l - p
            if p == tr - tl:
                return 0

            result = 0
            tc = (tl + tr) // 2

            if node.left and l < tc:
                result += count(node.left, tl, tc, l, min(tc, r), node.arr[p].left_link)

            if node.right and r > tc:
                result += count(node.right, tc, tr, max(tc, l), r, node.arr[p].right_link)

            return result

        def lower_bound(arr, x):
            l, r = 0, len(arr) - 1
            result = 0

            while l <= r:
                c = (l + r) // 2
                if arr[c] < x:
                    result = c + 1
                    l = c + 1
                else:
                    r = c - 1

            return result

        def lower_bound_data(arr, x):
            l, r = 0, len(arr) - 1
            result = 0

            while l <= r:
                c = (l + r) // 2
                if arr[c].value < x:
                    result = c + 1
                    l = c + 1
                else:
                    r = c - 1

            return result

        def upper_bound(arr, x):
            l, r = 0, len(arr) - 1
            result = 0

            while l <= r:
                c = (l + r) // 2
                if arr[c] <= x:
                    result = c + 1
                    l = c + 1
                else:
                    r = c - 1

            return result

        def pcc_array(x, y):
            n = len(x)
            res = [0] * n

            t = Node()
            initialize(t)
            add(t, 0, n, y)

            for i in range(n):
                p = lower_bound(x, x[i] + 1)
                if p < n:
                    q = lower_bound_data(t.arr, y[i])
                    res[i] += (n - p - count(t, 0, n, p, n, q))

                p = upper_bound(x, x[i] - 1)
                if p > 0:
                    q = lower_bound_data(t.arr, y[i] + 1)
                    res[i] += count(t, 0, n, 0, p, q)

            return res

        def _pcc_array(x, y):
            n = x.size
            res = np.zeros(n, dtype=np.intp)

            t = Node()
            initialize(t)
            add(t, 0, n, y)

            for i in range(n):
                p = lower_bound(x, x[i] + 1)
                if p < n:
                    q = lower_bound_data(t.arr, y[i])
                    res[i] += (n - p - count(t, 0, n, p, n, q))

                p = upper_bound(x, x[i] - 1)
                if p > 0:
                    q = lower_bound_data(t.arr, y[i] + 1)
                    res[i] += count(t, 0, n, 0, p, q)

            return res

        def _ranking(x: np.ndarray, y: np.ndarray, ordered: bool = False) -> tuple[Any, Any, Any | None, Any | None] | \
                                                                             tuple[Any, Any]:
            p = np.argsort(y, kind="mergesort")
            x, y = x[p], y[p]
            y = np.r_[True, y[1:] != y[:-1]].cumsum()

            y_ord = None
            if ordered:
                y_ord = y

            p = np.argsort(x, kind="mergesort")
            x, y = x[p], y[p]
            x = np.r_[True, x[1:] != x[:-1]].cumsum()

            x_ord = None
            if ordered:
                x_ord = x

            if ordered:
                return x, y, x_ord, y_ord
            else:
                return x, y

        def _pcc_pair(x: np.ndarray, y: np.ndarray) -> float:
            x, y = _ranking(x, y)
            x -= 1
            y -= 1
            n = x.shape[0]
            arr = np.array(_pcc_array(x, y))
            pcc_local = np.sum((n - 1 - arr) * (n - 2 - arr))
            return pcc_local / (n * (n - 1) * (n - 2))

        def pcc(x1: np.ndarray, x2: np.ndarray) -> float:
            x1 = np.array(x1).T
            x2 = np.array(x2).T

            return _pcc_pair(x1, x2)

        Xi = self.stocks_profitability[i]
        Xj = self.stocks_profitability[j]
        return pcc(Xi, Xj)

    # Функция для вычисления статистики Tij
    def calc_Tij_Kd(self, i, j, gamma_0):
        gamma_ij_Kd = self.G[i][j]

        P_c = self.calc_Pc(i, j)
        P_cc = self.calc_Pcc(i, j)
        self.Pcc.append(P_cc)

        difference = P_cc - (P_c ** 2)
        if difference < 0:
            difference = 0

        numerator = gamma_ij_Kd - gamma_0

        denumerator = 4 * (difference ** 0.5)
        if denumerator == 0:
            return 0

        return (self.observations_number ** 0.5) * (numerator / denumerator)

    # Функция для получения статистик T
    def calc_T_Kd(self):
        for gamma_0 in self.x_points:
            if gamma_0 not in self.T:
                self.T[gamma_0] = []
            for i in range(self.size_T):
                line = []
                for j in range(self.size_T):
                    line.append(self.calc_Tij_Kd(i, j, gamma_0))
                self.T[gamma_0].append(line)
