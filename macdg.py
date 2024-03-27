import pandas as pd
import matplotlib.pyplot as plt


class Wallet:
    money = 1000
    number_of_actions = 0

    def __init__(self):
        self.money = 1000
        self.number_of_actions = 0

    def buy_signal(self, price_of_action):
        self.number_of_actions = self.money / price_of_action
        self.money = 0
        return self

    def sell_signal(self, price_of_action):
        self.money = self.number_of_actions * price_of_action
        self.number_of_actions = 0
        return self
        

class MACD:
    def __init__(self, data, short_period=12, long_period=26, signal_period=9):
        self.data = data
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.macd_line = self.calculate_macd_line()
        self.signal_line = self.calculate_signal_line()

    def count_eman_arr(self, series, n):
        to_return = []
        for i in range(len(series)):
            numerator = 0
            denominator = 0
            alfa = 2 / (n + 1)
            one_minus_alfa = 1 - alfa
            if i < n - 1:
                to_return.append(None)
                continue
            if i >= len(series):
                return pd.Series(to_return, index=[i for i in range(len(to_return))])
            for j in range(n):
                t = series.iloc[j + i - n]
                numerator += t * one_minus_alfa**j
                denominator += one_minus_alfa**j
            to_return.append(numerator / denominator)
        return pd.Series(to_return, index=[i for i in range(len(to_return))])

    def calculate_ema(self, series, n):
        my = self.count_eman_arr(series, n)
        print(my)
        x = series.ewm(span=n, min_periods=n).mean()
        print(x)
        return my

    def calculate_macd_line(self):
        short_ema = self.calculate_ema(self.data['Otwarcie'], self.short_period)
        long_ema = self.calculate_ema(self.data['Otwarcie'], self.long_period)
        return short_ema - long_ema

    def calculate_signal_line(self):
        return self.calculate_ema(self.macd_line, self.signal_period)

    def plot_macd(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['Data'], self.data['Otwarcie'], label='Otwarcie', color='blue')
        plt.title('Wykres ceny z wskaźnikiem MACD')
        plt.xlabel('Data')
        plt.ylabel('Cena')
        plt.legend(loc='upper left')

        plt.twinx()
        plt.plot(self.data['Data'], self.macd_line, label='Linia MACD', color='red')
        plt.plot(self.data['Data'], self.signal_line, label='Linia sygnałowa', color='green')
        plt.legend(loc='upper right')
        plt.show()

    def generate_signals(self):
        signals = []
        positions = []  # 1 for long, -1 for short, 0 for hold
        for i in range(1, len(self.signal_line)):
            if self.macd_line[i] > self.signal_line[i] and self.macd_line[i-1] <= self.signal_line[i-1]:
                signals.append(self.data['Data'][i])
                positions.append(1)  # Sygnał kupna
            elif self.macd_line[i] < self.signal_line[i] and self.macd_line[i-1] >= self.signal_line[i-1]:
                signals.append(self.data['Data'][i])
                positions.append(-1)  # Sygnał sprzedaży
            else:
                # positions.append(0)  # Hold
                pass
        return signals, positions

    def plot_signals(self, signals, positions):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['Data'], self.data['Otwarcie'], label='Otwarcie', color='blue')
        plt.title('Wykres ceny z sygnałami MACD')
        plt.xlabel('Data')
        plt.ylabel('Cena')

        # Rozdzielenie sygnałów na kupno i sprzedaż
        buy_signals = [signal for signal, position in zip(signals, positions) if position == 1]
        sell_signals = [signal for signal, position in zip(signals, positions) if position == -1]

        plt.scatter(buy_signals, self.data[self.data['Data'].isin(buy_signals)]['Otwarcie'], marker='^', color='green', label='Sygnały kupna')
        plt.scatter(sell_signals, self.data[self.data['Data'].isin(sell_signals)]['Otwarcie'], marker='v', color='red', label='Sygnały sprzedaży')
        plt.legend()
        plt.show()

# Wczytaj dane z pliku CSV
# data = pd.read_csv('wig20.csv')
data = pd.read_csv('nvidia.csv')
data['Data'] = pd.to_datetime(data['Data'])  # Konwersja kolumny daty na typ datetime

# Utwórz instancję klasy MACD i oblicz wskaźniki MACD oraz sygnału
macd_indicator = MACD(data)

# Wygeneruj i wyświetl sygnały kupna/sprzedaży oraz wykresy
signals, positions = macd_indicator.generate_signals()
macd_indicator.plot_signals(signals, positions)
macd_indicator.plot_macd()
wallet = Wallet()
if positions[0] == -1:
    signals == signals.pop(0)
    positions == positions.pop(0)

for signal, position in zip(signals, positions):
    if position == 1:  # Buy signal
        print(f"Bought 1 stock at {data[data['Data'] == signal]['Otwarcie'].values[0]}, Data: {signal}")
        wallet = wallet.buy_signal(data[data['Data'] == signal]['Otwarcie'].values[0])
    elif position == -1:  # Sell signal
        print(f"Sold 1 stock at {data[data['Data'] == signal]['Otwarcie'].values[0]}, Data: {signal}")
        wallet = wallet.sell_signal(data[data['Data'] == signal]['Otwarcie'].values[0])

wallet = wallet.sell_signal(data[data['Data'] == signals[-1]]['Otwarcie'].values[0])
print(wallet.money)
