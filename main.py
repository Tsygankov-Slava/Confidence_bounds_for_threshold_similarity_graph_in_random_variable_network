import os

from calculations.K import K
from calculations.T_Kd import T_Kd
from calculations.T_P import T_P
from Show import Show
from auxiliary.frange import frange
from calculations.AuxiliarySets import AuxiliarySets

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

import shelve
cache_filename = "cache"
db = shelve.open(cache_filename)

x_low = -0.8
x_high = 1
step = 0.05

x_points = [round(x, 2) for x in frange(x_low, x_high, step)]

stock_names_to_shortcut = {
    "Australia market": "ASX",

    # Asian
    "China market": "HKEX",
    "India market": "NSE",
    "Japan market": "TSE",

    # America
    "USA market": "NYSE",
    "Canada market": "TSX",
    "Argentina market": "BCBA",
    "Brazil market": "B3",

    # Europe
    "UK market": "LSE",
    "Italy market": "ISE",
    "Spain market": "BME",
    "Sweden market": "OMXS30",
}

daily_data_close_csv_file_names = {
    "Australia market" : "data_loading/Australia/Australia_daily_close_prices_2023.csv",

    #Asian
    "China market" : "data_loading/China/China_daily_close_prices_2023.csv",
    "India market" : "data_loading/India/India_daily_close_prices_2023.csv",
    "Japan market" : "data_loading/Japan/Japan_daily_close_prices_2023.csv",

    #America
    "USA market" : "data_loading/USA/USA_daily_close_prices_2023.csv",
    "Canada market" : "data_loading/Canada/Canada_daily_close_prices_2023.csv",
    "Argentina market" : "data_loading/Argentina/Argentina_daily_close_prices_2023.csv",
    "Brazil market" : "data_loading/Brazil/Brazil_daily_close_prices_2023.csv",

    # Europe
    "UK market" : "data_loading/UK/UK_daily_close_prices_2023.csv",
    "Italy market" : "data_loading/Italy/Italy_daily_close_prices_2023.csv",
    "Spain market" : "data_loading/Spain/Spain_daily_close_prices_2023.csv",
    "Sweden market" : "data_loading/Sweden/Sweden_daily_close_prices_2023.csv",
}

def save_tex_table(filename, latex_table):
    os.makedirs('Data_For_Article/Tables/tex/', exist_ok=True)
    with open(f'Data_For_Article/Tables/tex/{filename}.tex', 'w') as f:
        f.write(latex_table)

def generate_all(K1_P, K1_Kd, K2_P, K2_Kd, title, filename):
    latex_table = r"""
\begin{tabular}{ |c|c|c|c|c| }
\hline
& \multicolumn{2}{|c|}{Kendall} & \multicolumn{2}{|c|}{Pearson} \\
\cline{2-5}
\raisebox{1.5ex}{Markets} & $K_1^i$ & $K_2^i$ & $K_1^i$ & $K_2^i$ \\
\hline
    """

    for key in K1_P.keys():
        latex_table += f"{key.split()[0]} & {K1_Kd[key]} & {K2_Kd[key]} & {K1_P[key]} & {K2_P[key]} \\\\ \n \hline \n"

    latex_table += r"""\end{tabular}"""

    save_tex_table(filename, latex_table)

def generate_groups_for_K1i(K1i):
    K1i_values = list(K1i.values())
    groups = {}

    for key, value in K1i.items():
        key = key.split()[0]
        if value in groups:
            groups[value].append(key)
        else:
            if K1i_values.count(value) > 1:
                groups[value] = [key]
    return groups

def generate_groups_for_K2i(K2i, intervals):
    groups = {str(i): [] for i in intervals}

    K2i_sorted = dict(sorted(K2i.items()))
    for key, value in K2i_sorted.items():
        key = key.split()[0]
        for interval in intervals:
            if interval[0] <= value < interval[1]:
                groups[str(interval)].append((key, round(value, 2)))
    return groups

def generate_K2i(groups, title, filename):
    latex_table = r"""
\begin{table}[ph]
\centering
\small
\begin{tabular}{ |c|c| }
\hline
& Markets \\
\hline
    """

    for key, value in groups.items():
        if len(value) > 1:
            markets = ', '.join([f"{country}({value})" for country, value in value])
            latex_table += f"{key.replace('(', '[')} & {markets} \\\\ \n \hline \n"
    latex_table += r"""\end{tabular}
\caption{""" + title + """}
\end{table}""" + "\n\n"

    save_tex_table(filename, latex_table)


def generate_K1i(groups, coef_name, title, filename):
    latex_table = r"""
\begin{table}[ph]
\centering
\begin{tabular}{ |c|c| }
\hline
""" + coef_name + """ & Markets \\\\
\hline
    """

    for key, value in dict(sorted(groups.items())).items():
        markets = ", ".join(value)
        latex_table += f"{key} & {markets} \\\\ \n \hline \n"
    latex_table += r"""\end{tabular}
\caption{""" + title + """}
\end{table}""" + "\n\n"

    save_tex_table(filename, latex_table)

def generate_K1i_P_Kd(groups_P, groups_Kd, title, filename):
    latex_table = r"""
\begin{table}[ph]
\centering
\small
\begin{tabular}{ |c|c| }
\hline
& Markets \\
\hline
    """

    for keyP, valueP in groups_P.items():
        for keyKd, valueKd in groups_Kd.items():
            markets = ", ".join(list(set(valueP) & set(valueKd)))
            latex_table += f"Kendall: {keyKd}, Pearson: {keyP} & {markets} \\\\ \n \hline \n"

    latex_table += r"""\end{tabular}
    \caption{""" + title + """}
    \end{table}""" + "\n\n"

    save_tex_table(filename, latex_table)

def generate_K2i_P_Kd(groups_P, groups_Kd, title, filename):
    latex_table = r"""
\begin{table}[ph]
\centering
\small
\begin{tabular}{ |c|c| }
\hline
& Markets \\
\hline
    """

    for keyP, valueP in groups_P.items():
        for keyKd, valueKd in groups_Kd.items():
            intersection = [itemP[0] for itemP in valueP if itemP[0] in (itemKd[0] for itemKd in valueKd)]
            if intersection:
                markets = ", ".join(intersection)
                latex_table += f"Kendall: {keyKd.replace('(', '[')}, Pearson: {keyP.replace('(', '[')} & {markets} \\\\ \n \hline \n"

    latex_table += r"""\end{tabular}
    \caption{""" + title + """}
    \end{table}""" + "\n\n"

    save_tex_table(filename, latex_table)

def generate_table_for_gamma(Ki, gamma, filename):
    result = {}
    for market, values in Ki.items():
        result[market] = values.get(gamma, None)

    latex_table = r"""
\begin{table}[H]
\centering
\begin{tabular}{ | c | c | }
\hline
    & Market & Ki \\
\hline
        """

    for market, value in result.items():
        latex_table += f"\t\t{market} & {round(value, 2)} \\\\ \\hline\n"

    latex_table += r"""\end{tabular}
\end{table}""" + "\n\n"

    save_tex_table(filename, latex_table)

show = Show(x_points)

G_TP = {}
G_TKd = {}

K1_P = {}
K1_Kd = {}

K2_P = {}
K2_Kd = {}

K1i_P = {}
K2i_P = {}
K1i_Kd = {}
K2i_Kd = {}

tickers_to_csv_list = [
    (merval_tickers, "Argentina/Argentina_daily_close_prices_2023.csv", "BCBA"),
    (asx50_tickers, "Australia/Australia_daily_close_prices_2023.csv", "ASX"),
    (ibov_tickers, "Brazil/Brazil_daily_close_prices_2023.csv", "B3"),
    (tsx_tickers, "Canada/Canada_daily_close_prices_2023.csv", "TSX"),
    (hang_seng_tickers, "China/China_daily_close_prices_2023.csv", "HKEX"),
    (nifty_tickers, "India/India_daily_close_prices_2023.csv", "NSE"),
    (ftse_mib_tickers, "Italy/Italy_daily_close_prices_2023.csv", "Borsa Italiana"),
    (nikkei_225_tickers, "Japan/Japan_daily_close_prices_2023.csv", "TSE"),
    (ibex_35_tickers, "Spain/Spain_daily_close_prices_2023.csv", "BME"),
    (omx_stockholm_30_tickers, "Sweden/Sweden_daily_close_prices_2023.csv", "OMXS30"),
    (ftse_100_tickers, "UK/UK_daily_close_prices_2023.csv", "LSE"),
    (djia_tickers, "USA/USA_daily_close_prices_2023.csv", "NYSE"),
]

for tickers_to_csv in tickers_to_csv_list:
    tickers = tickers_to_csv[0]
    csv_file_name = tickers_to_csv[1]
    stock_name_shortcut = tickers_to_csv[2]
    print(f"{csv_file_name.split('/')[0]} -> {len(tickers)} -> {len(tickers) * (len(tickers) - 1) // 2}")

for stock_name, daily_data_close_csv_file_name in daily_data_close_csv_file_names.items():
    directory = f"Data_For_Article/Graphics/Countries/{stock_name}"
    os.makedirs(directory, exist_ok = True)

    ###### Раздел Пирсона ######
    print(f"--{stock_name}--")
    T_p = T_P(daily_data_close_csv_file_name, x_points)

    auxiliarySetsForTP = AuxiliarySets(x_points, T_p)
    for gamma_0 in x_points:
        auxiliarySetsForTP.calc_Le(gamma_0)
        auxiliarySetsForTP.calc_Ue(gamma_0)
        auxiliarySetsForTP.calc_G(gamma_0)
    auxiliarySetsForTP.calc_Ln()
    auxiliarySetsForTP.calc_Un()

    for gamma_0 in x_points:
        auxiliarySetsForTP.check_G(gamma_0)

    G_TP[stock_name] = auxiliarySetsForTP.G

    K_P = K(auxiliarySetsForTP.G, auxiliarySetsForTP.Le, auxiliarySetsForTP.Ln, len(auxiliarySetsForTP.J), stock_name, len(x_points))
    K1_P[stock_name] = K_P.K1
    K2_P[stock_name] = K_P.K2

    K1i_P[stock_name] = round(K_P.K1_i, 2)
    K2i_P[stock_name] = round(K_P.K2_i, 2)
    print(f"{stock_name} (K={K_P.K}) -> K1_i: {K_P.K1_i} | K2_i: {K_P.K2_i}")



    show.show_Ue_Le(auxiliarySetsForTP.Ue, auxiliarySetsForTP.Le,
                    suptitle=stock_name,
                    title=r"Pearson Correlation ($\mathcal{P}^*$=0.9)",
                    graphic_name="Dependence_Le_Ue_(Pearson_Correlation)")

    show.get_gist([T_p.R[i][j] for i in range(len(T_p.R)) for j in range(i + 1, len(T_p.R[i]))],
                  title=stock_name,
                  xlabel='Pearson Correlation Coefficient',
                  graphic_name="Histogram_(Pearson_Correlation_Coefficient)")

    ###### Раздел Кенделла ######
    key = f"{daily_data_close_csv_file_name}_TKd"
    if key in db:
        T_kd = db[key]
    else:
        T_kd = T_Kd(daily_data_close_csv_file_name, x_points)
        db[key] = T_kd

    auxiliarySetsForTKd = AuxiliarySets(x_points, T_kd)
    for gamma_0 in x_points:
        auxiliarySetsForTKd.calc_Le(gamma_0)
        auxiliarySetsForTKd.calc_Ue(gamma_0)
        auxiliarySetsForTKd.calc_G(gamma_0)
    auxiliarySetsForTKd.calc_Ln()
    auxiliarySetsForTKd.calc_Un()

    for gamma_0 in x_points:
        auxiliarySetsForTKd.check_G(gamma_0)

    G_TKd[stock_name] = auxiliarySetsForTKd.G

    K_Kd = K(auxiliarySetsForTKd.G, auxiliarySetsForTKd.Le, auxiliarySetsForTKd.Ln, len(auxiliarySetsForTKd.J), stock_name, len(x_points))
    K1_Kd[stock_name] = K_Kd.K1
    K2_Kd[stock_name] = K_Kd.K2

    K1i_Kd[stock_name] = round(K_Kd.K1_i, 2)
    K2i_Kd[stock_name] = round(K_Kd.K2_i, 2)
    print(f"{stock_name} (K={K_Kd.K}) -> K1_i: {K_Kd.K1_i} | K2_i: {K_Kd.K2_i}")

    show.show_Ue_Le(auxiliarySetsForTKd.Ue, auxiliarySetsForTKd.Le,
                    suptitle=stock_name,
                    title=r"Kendall Correlation ($\mathcal{P}^*$=0.9)",
                    graphic_name="Dependence_Le_Ue_(Kendall Correlation)")


    show.get_gist([T_kd.G[i][j] for i in range(len(T_kd.G)) for j in range(i + 1, len(T_kd.G[i]))],
                  title=stock_name,
                  xlabel="Kendall Correlation Coefficient",
                  graphic_name="Histogram_(Kendall_Correlation_Coefficient)")

    show.show_K(K_P.K1, K_Kd.K1, title=stock_name, graphic_name="Dependence_K1")
    show.show_K(K_P.K2, K_Kd.K2, title=stock_name, graphic_name="Dependence_K2")

keys = list(K1i_P.keys())
keys_shortcut = []
for key in keys:
    keys_shortcut.append(stock_names_to_shortcut[key])

generate_all(K1i_P, K1i_Kd, K2i_P, K2i_Kd, r"""""", "Ki")

groups_K1i_P = generate_groups_for_K1i(K1i_P)
generate_K1i(groups_K1i_P, r"""$K_1^i$ Pearson""", r"""Groups of $K_1^i$ Pearson""", "K1i")

groups_K1i_Kd = generate_groups_for_K1i(K1i_Kd)
generate_K1i(groups_K1i_Kd, r"""$K_1^i$ Kendall""", r"""Groups of $K_1^i$ Kendall""", "K1i")

groups_K2i_P = generate_groups_for_K2i(K2i_P, [(0.6, 1)])
generate_K2i(groups_K2i_P, r"""Groups of $K_2^i$ Pearson""", "K2i")

groups_K2i_Kd = generate_groups_for_K2i(K2i_Kd, [(0.4, 0.6)])
generate_K2i(groups_K2i_Kd, r"""Groups of $K_2^i$ Kendall""", "K2i")

generate_table_for_gamma(K2_Kd, 0.2, "K2i_Kd_gamma_0,2")
generate_table_for_gamma(K1_P, 0.25, "K1i_P_gamma_0,25")

generate_K1i_P_Kd(groups_K1i_P, groups_K1i_Kd, r"""Groups of $K_1^i$ Kendall and $K_1^i$ Pearson""", "K1i_P_and_Kd")
generate_K2i_P_Kd(groups_K2i_P, groups_K2i_Kd, r"""Groups of $K_2^i$ Kendall and $K_2^i$ Pearson""", "K2i_P_and_Kd")
show.show_G(G_TP, title="Pearson Correlation",
                graphic_name="Dependence_G_(Pearson_Correlation)_All")
show.show_G(G_TKd, title="Kendall Correlation",
                graphic_name="Dependence_G_(Kendall_Correlation)_All")

show.show_K_All(K1_P, graphic_name="Dependence_K1_(Pearson_Correlation)_All")
show.show_K_All(K1_Kd, graphic_name="Dependence_K1_(Kendall_Correlation)_All")

show.show_K_All(K2_P, graphic_name="Dependence_K2_(Pearson_Correlation)_All")
show.show_K_All(K2_Kd, graphic_name="Dependence_K2_(Kendall_Correlation)_All")

# Table 2
for K1_item, stock_markets in groups_K1i_P.items():
    show.show_K_Selectively(K1_P, stock_markets, str(K1_item),
                            graphic_name=f"Dependence_K1_(Pearson_Correlation)_K1_{K1_item}_Table2")
# Table 3
for K1_item, stock_markets in groups_K1i_Kd.items():
    show.show_K_Selectively(K1_Kd, stock_markets, str(K1_item),
                            graphic_name=f"Dependence_K1_(Kendall_Correlation)_K1_{K1_item}_Table3")

# Table 4
for K2_item, stock_markets in groups_K2i_P.items():
    if len(stock_markets) > 1:
        stock_markets = [i[0] for i in stock_markets]
        show.show_K_Selectively(K2_P, stock_markets, str(K2_item),
                            graphic_name=f"Dependence_K2_(Pearson_Correlation)_K2_{K2_item}_Table4")

# Table 5
for K2_item, stock_markets in groups_K2i_Kd.items():
    if len(stock_markets) > 1:
        stock_markets = [i[0] for i in stock_markets]
        show.show_K_Selectively(K2_Kd, stock_markets, str(K2_item),
                            graphic_name=f"Dependence_K2_(Kendall_Correlation)_K2_{K2_item}_Table5")

# Table 6
for keyP, valueP in groups_K1i_P.items():
    for keyKd, valueKd in groups_K1i_Kd.items():
        markets = list(set(valueP) & set(valueKd))
        if len(markets) > 1:
            show.show_K_Selectively(K1_P, markets, f"P{keyP}_Kd{keyKd}",
                                    graphic_name=f"Dependence_K1_P_P{keyP}_Kd{keyKd}_Table6")
            show.show_K_Selectively(K1_Kd, markets, f"P{keyP}_Kd{keyKd}",
                                    graphic_name=f"Dependence_K1_Kd_P{keyP}_Kd{keyKd}_Table6")
# Table 7
for keyP, valueP in groups_K2i_P.items():
    for keyKd, valueKd in groups_K2i_Kd.items():
        markets = [itemP[0] for itemP in valueP if itemP[0] in (itemKd[0] for itemKd in valueKd)]
        if len(markets) > 1:
            show.show_K_Selectively(K2_P, markets, f"P{keyP}_Kd{keyKd}",
                                    graphic_name=f"Dependence_K2_P_P{keyP}_Kd{keyKd}_Table7")
            show.show_K_Selectively(K2_Kd, markets, f"P{keyP}_Kd{keyKd}",
                                    graphic_name=f"Dependence_K2_Kd_P{keyP}_Kd{keyKd}_Table7")
