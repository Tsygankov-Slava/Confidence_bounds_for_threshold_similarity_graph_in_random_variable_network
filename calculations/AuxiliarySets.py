class AuxiliarySets:
    def __init__(self, x_points, statistics):
        self.x_points = x_points
        self.statistics = statistics
        self.N = self.statistics.size_T

        self.J = set()
        self.calc_J()

        self.Ue = {}
        self.Le = {}
        self.Un = {}
        self.Ln = {}
        self.G = {}

    def calc_J(self):
        for i in range(self.N):
            for j in range(i + 1, self.N):
                self.J.add((i, j))

    def calc_Ue(self, gamma_0):
        local_Ue = set()
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.statistics.T[gamma_0][i][j] >= self.statistics.c_ij_e:
                    local_Ue.add((i, j))
        self.Ue[gamma_0] = local_Ue

    def calc_Le(self, gamma_0):
        local_Le = set()
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.statistics.T[gamma_0][i][j] > self.statistics.c_ij_n:
                    local_Le.add((i, j))
        self.Le[gamma_0] = local_Le

    def calc_Ln(self):
        for gamma_0, values in self.Ue.items():
            self.Ln[gamma_0] = list(self.J - self.Ue[gamma_0])

    def calc_Un(self):
        for gamma_0, value in self.Le.items():
            self.Un[gamma_0] = list(self.J - self.Le[gamma_0])

    def calc_G(self, gamma_0):
        self.G[gamma_0] = list(set(self.Ue[gamma_0] - self.Le[gamma_0]))

    def check_G(self, gamma_0):
        first = set(self.Ue[gamma_0]) - set(self.Le[gamma_0])
        second = set(self.Un[gamma_0]) - set(self.Ln[gamma_0])
        if first != second:
            print(f"Set is NOT equal for gamma_0 = {gamma_0}")
            print(f"Ue - Le = {first}")
            print(f"Un - Ln = {second}")
            s = first - second
            print(f"INFO: {s}")
            for el in s:
                print(f"Tij({el[0]})({el[1]})[{gamma_0}] = {self.statistics.T[gamma_0][el[0]][el[1]]}, cij_e = {self.statistics.c_ij_e}, cij_n = {self.statistics.c_ij_n}")
            print("\n\n")

