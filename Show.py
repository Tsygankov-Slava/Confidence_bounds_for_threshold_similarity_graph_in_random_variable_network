import os

import numpy as np
from matplotlib import pyplot as plt


class Show:
    def __init__(self, x_points):
        self.x_points = x_points

        self.path_to_graphics_dir = "Data_For_Article/Graphics/Countries"
        os.makedirs(self.path_to_graphics_dir, exist_ok = True)

    def generate_name(self, stock_name="", graphic_name="", path=""):
        if path == "":
            path = f"{self.path_to_graphics_dir}/{stock_name}"
        os.makedirs(path, exist_ok=True)
        return f"{path}/{graphic_name}.png"

    def get_gist(self, data, title="", xlabel="", graphic_name=""):
        data = np.asarray(data)

        plt.figure(figsize=(10, 6))
        counts, bins, patches = plt.hist(data, bins=20, edgecolor='black')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel('Frequency')

        bin_centers = 0.5 * (bins[1:] + bins[:-1])

        bin_means = []
        for i in range(len(bins) - 1):
            bin_data = data[(data >= bins[i]) & (data < bins[i + 1])]
            if len(bin_data) > 0:
                bin_means.append(np.mean(bin_data))

            else:
                bin_means.append(0)

        for count, x in zip(counts, bin_centers):
            if count > 0:
                plt.text(x, count + 0.1, str(int(count)), color="blue", ha='center')

        non_zero_means = []
        non_zero_centers = []
        for i in range(len(bin_means)):
            if bin_means[i] != 0:
                non_zero_means.append(bin_means[i])
                non_zero_centers.append(bin_centers[i])

        plt.xticks(non_zero_centers, [f'{mean:.2f}' for mean in non_zero_means], fontsize=8)

        plt.grid(axis='y', alpha=0.75)

        plt.savefig(self.generate_name(stock_name=title, graphic_name=graphic_name), format='png')

        plt.show(block=False)
        plt.close()

    def show_Ue_Le(self, Ue, Le, suptitle="", title="", graphic_name=""):
        local_Ue = []
        for key, value in Ue.items():
            local_Ue.append(len(value))

        local_Le = []
        for _, value in Le.items():
            local_Le.append(len(value))

        plt.plot(self.x_points, local_Ue, color='blue', marker='o', linestyle='-', markersize=3, linewidth=1,
                 label=r'$| U_e(\mathcal{x}, \gamma_0, \mathcal{P}^*) |$')
        plt.plot(self.x_points, local_Le, color='red', marker='o', linestyle='--', markersize=3, linewidth=1,
                 label=r'$| L_e(\mathcal{x}, \gamma_0, \mathcal{P}^*) |$')

        first_x_value = self.x_points[0]
        first_y_value = local_Ue[0]

        plt.annotate(f'{first_y_value}',
                     xy=(first_x_value, first_y_value),
                     xytext=(0, 6),
                     textcoords='offset points',
                     fontsize=9,
                     color='black',
                     ha='center',
                     va='center')

        plt.suptitle(suptitle)
        plt.title(title)

        plt.xlabel(r'$\gamma_0$')

        plt.legend(fontsize=12)

        plt.savefig(self.generate_name(stock_name=suptitle, graphic_name=graphic_name), format='png')

        plt.show(block=False)
        plt.close()

    def show_G(self, G, title = "", graphic_name = ""):
        line_styles = ['-', '--', '-.', ':']
        style_index = 0

        for stock_name, dict_ in G.items():
            l = []
            for _, list_ in dict_.items():
                l.append(len(list_))
            plt.plot(self.x_points, l, marker='o', label=stock_name, linestyle=line_styles[style_index % len(line_styles)])
            style_index += 1

        plt.title(title)

        plt.xlabel(r'$\gamma_0$')
        plt.ylabel(r'$| G(\mathcal{x}, \gamma_0, \mathcal{P}^*) |$')

        plt.grid()

        plt.legend(fontsize=12)

        plt.savefig(self.generate_name(stock_name="", graphic_name=graphic_name), format='png')

        plt.show(block=False)
        plt.close()

    def show_K(self, K_P, K_Kd, title = "", graphic_name = ""):
        K_P = [value for key, value in K_P.items()]
        K_Kd = [value for key, value in K_Kd.items()]
        plt.plot(self.x_points, K_P, color='orange', marker='o', linestyle='-', markersize=3, linewidth=1,
                 label="Pearson correlation coefficient")
        plt.plot(self.x_points, K_Kd, color='blue', marker='o', linestyle='--', markersize=3, linewidth=1,
                 label="Kendall correlation coefficient")

        plt.title(title)

        plt.xlabel(r'$\gamma_0$')

        plt.legend(fontsize=12)

        plt.savefig(self.generate_name(stock_name=title, graphic_name=graphic_name), format='png')

        plt.show(block=False)
        plt.close()

    def show_K_All(self, K, graphic_name=""):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'pink', 'brown', 'gray']
        markers = ['o', 's', '^', 'D', 'x', '*', '+', 'P', '|', '_']
        linestyles = ['-', '--', '-.', ':']

        if 'Argentina market' in K:
            del K['Argentina market']

        for i, (stock_name, K_values) in enumerate(K.items()):
            marker = markers[i % len(markers)]
            linestyle = linestyles[i % len(linestyles)]

            plt.plot(self.x_points, [value for key, value in K_values.items()],
                     marker=marker,
                     linestyle=linestyle,
                     markersize=5,
                     linewidth=1,
                     label=stock_name)

        plt.xlabel(r'''$\gamma_0$''')
        plt.legend(fontsize=12)

        plt.savefig(self.generate_name(stock_name="", graphic_name=graphic_name))

        plt.show(block=False)
        plt.close()

    def show_K_Selectively(self, K, stock_markets, stock_markets_name, graphic_name=""):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'pink', 'brown', 'gray']

        for stock_name in stock_markets:
            stock_name = f"{stock_name} market"
            if stock_name in K:
                K_values = K[stock_name]
                color = colors[stock_markets.index(stock_name.split()[0]) % len(colors)]

                plt.plot(self.x_points, [value for key, value in K_values.items()],
                         color=color,
                         marker='o',
                         linestyle='-',
                         markersize=3,
                         linewidth=1,
                         label=stock_name)

        plt.title(graphic_name)
        plt.suptitle(stock_markets_name)
        plt.xlabel(r'$\gamma_0$')
        plt.savefig(self.generate_name(stock_name=stock_markets_name, graphic_name=f"{graphic_name}", path="Data_For_Article/Graphics/For_Tables"), format='png')
        plt.show(block=False)
        plt.close()

    def show_G_Selectively(self, G, stock_markets, stock_markets_name, title="", graphic_name=""):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'pink', 'brown', 'gray']

        for stock_name in stock_markets:
            if stock_name in G:
                dict_ = G[stock_name]
                l = [len(list_) for _, list_ in dict_.items()]

                color = colors[stock_markets.index(stock_name) % len(colors)]
                plt.plot(self.x_points, l, marker='o', label=stock_name, linestyle='-', color=color)

        plt.title(title)
        plt.suptitle(stock_markets_name)
        plt.xlabel(r'$\gamma_0$')
        plt.ylabel(r'$| G(\mathcal{x}, \gamma_0, \mathcal{P}^*) |$')
        plt.grid()
        plt.legend(fontsize=12)

        plt.savefig(self.generate_name(stock_name=stock_markets_name, graphic_name=graphic_name), format='png')
        plt.show(block=False)
        plt.close()