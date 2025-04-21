class K:
    def __init__(self, G, Le, Ln, M, stock_name, K_):
        self.G = G
        self.Le = Le
        self.Ln= Ln
        self.M = M
        self.stock_name = stock_name

        self.K = K_
        self.cs = 1 / self.K

        self.K1 = {}
        self.K2 = {}

        self.get_K1()
        self.get_K2()

        self.K1_i = 0
        self.K2_i = 0

        self.get_K1_i()
        self.get_K2_i()

    def get_K1(self):
        for key, value in self.G.items():
            self.K1[key] = len(value) / self.M

    def get_K2(self):
        for key, value in self.G.items():
            a = len(set(self.Le[key]) | set(self.Ln[key]))
            if a == 0:
                self.K2[key] = 0
            else:
                self.K2[key] = len(value) / a

    def get_K1_i(self):
        res = 0
        K1_values = list(self.K1.values())
        for i in range(self.K):
            res += self.cs * K1_values[i]
        self.K1_i = res


    def get_K2_i(self):
        res = 0
        K2_values = list(self.K2.values())
        for i in range(self.K):
            res += self.cs * K2_values[i]
        self.K2_i = res