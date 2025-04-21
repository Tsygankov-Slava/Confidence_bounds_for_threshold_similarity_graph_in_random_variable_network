# Содержание
- [Описание проекта](#Описание-проекта)
- [Структура проекта](#Структура-проекта)
- [Запуск](#Запуск)
  - [Скачивание данных](#Скачивание-данных)
  - [Генерация графиков и таблиц](#Генерация-графиков-и-таблиц)

# Описание проекта
Программа создавалась в рамках статьи `"Uncertainty of threshold similarity graph identification in correlation-based market networks"`. Она выгружает данные с международных рынков акций и на их основе позволяет моментально (с использованием кеша) рассчитывать сложно вычислимые формулы и отображать различные графики, столбчатые диаграммы и генерировать tex-таблицы. Все это помогало при анализе результатов из статьи.


# Структура проекта
```
Confidence_bounds_for_threshold_similarity_graph_in_random_variable_network
│
├── auxiliary
│   └── frange.py
│
├── calculations
│   ├── AuxiliarySets.py
│   ├── K.py
│   ├── T_Kd.py
│   └── T_P.py
│
├── data_loading
│   ├── Argentina
│   │   ├── tickers.py
│   │   ├── Argentina_daily_close_prices_2023.csv
│   │   └── Argentina_daily_close_prices_2023_original.csv
│   │
│   ├── Australia
│   │   ├── tickers.py
│   │   ├── Australia_daily_close_prices_2023.csv
│   │   └── Australia_daily_close_prices_2023_original.csv
│   │
│   ...
│   │
│   └── tickers_loading.py
│
├── Data_For_Article
│   ├── Closing_Prices_Graphics
│       └── ...
│   ├── Graphics
│   │   ├── Countries
│           └── ...
│   │   ├── For_Tables
│           └── ...
│   │   └── Profitability
│           └── ...
│   └── Tables
│       └── tex
│           └── ...
│
├── cache.db
│
├── Data.py
├── Show.py
└── main.py

```

## Запуск
### Скачивание данных
Для скачивания данных нужно запустить файл [`tickers_loading.py`](data_loading/tickers_loading.py).

> [`tickers_loading.py`](data_loading/tickers_loading.py): Выгружает данные акций с помощью библиотеки `yfinance`, выбирает цены закрытия, сохраняет их в `.csv` файл и строит по этим данным графики, которые также сохраняет в `.png` в директорию `Data_For_Article/Closing_Prices_Graphics/`.

 В результате каждая страна имеет в директории `data_loading/"Name of country"/` два `.csv` файла: `"Name of country"_daily_close_prices_2023_original.csv` и `"Name of country"_daily_close_prices_2023.csv`.
 
`"Name of country"_daily_close_prices_2023_original.csv` - Это сырые данные. В столбцах могут быть пропуски, например, если для какой-то даты не было торгов.
 
`"Name of country"_daily_close_prices_2023.csv` - Это обработанные данные. Применяется линейная интерполяция, а к оставшимся пропускам `backward fill` + `forward fill`.

#### Генерация графиков и таблиц
Чтобы сгенерировать все графики и таблицы нужно запустить скрипт [`main.py`](main.py).
После его работы создастся директория `Data_For_Article` в которой будет вся сгенерированная информация.
- [`Data_For_Article/Graphics/Countries/`](Data_For_Article/Graphics/Countries/) - содержит графики для каждой страны в отдельности.
- [`Data_For_Article/Graphics/Profitability/`](Data_For_Article/Graphics/Profitability/) - содержит графики по доходностям для каждой страны в отдельности.
- [`Data_For_Article/Tables/tex/`](Data_For_Article/Tables/tex/) содержит сгенерированные tex-таблицы для статьи.
- [`Data_For_Article/Graphics/For_Tables/`](Data_For_Article/Graphics/For_Tables/) - содержит графики по таблицам из директории `Data_For_Article/Tables/tex/`.
