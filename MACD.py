import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy


def count_macd(data, n):
    ema12 = count_eman(n, 12, data)
    ema26 = count_eman(n, 26, data)
    return ema12 - ema26


def count_eman(first, n, data):
    l = 0
    m = 0
    alfa = 2 / (n+1)
    one_minus_alfa = 1 - alfa
    for i in range(n):
        if first + i > len(data):
            return l / m
        t = data.values[first + i][1]
        l += t * (one_minus_alfa).__pow__(i)
        m += one_minus_alfa.__pow__(i)
    return l / m


def count_eman_arr(first, n, data):
    l = 0
    m = 0
    alfa = 2 / (n+1)
    one_minus_alfa = 1 - alfa
    for i in range(n):
        if first + i > len(data):
            return l / m
        t = data[first + i]
        l += t * (one_minus_alfa).__pow__(i)
        m += one_minus_alfa.__pow__(i)
    return l / m


def left_stripe_data(data1, data2):
    if len(data1) > len(data2):
        diff = len(data1) - len(data2)
        data1 = data1[diff::]
    else:
        diff = len(data2) - len(data1)
        data2 = data2[diff::]
    return data1, data2


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


if __name__ == "__main__":
    data = pd.read_csv('nvidia.csv')
    data_dict = {}
    for tup in data.values:
        data_dict[tup[0]] = tup[1]
    macd = []
    macd_and_dates = []
    signal = []
    signal_and_dates = []

    for i in range(len(data) - 37):
        if i > 25:
            macd_to_add = count_macd(data, i)
            macd.append(macd_to_add)
            macd_and_dates.append((macd_to_add, data.values[i][0]))
        if i > 34:
            signal_to_add = count_eman_arr(i - 35, 9, macd)
            signal.append(signal_to_add)
            signal_and_dates.append((signal_to_add, data.values[i][0]))
    # data.plot()
    
    # plt.show()
    prices = data.values[:, 1]
    dates = data.values[:, 0]
    macd, signal = left_stripe_data(macd, signal)
    prices, macd = left_stripe_data(prices, macd)
    dates, prices = left_stripe_data(dates, prices)
    macd_and_dates, macd = left_stripe_data(macd_and_dates, macd)
    macd_and_dates, signal_and_dates = left_stripe_data(macd_and_dates, signal_and_dates)

    story_of_trades = []
    money_story = []
    wallet = Wallet()
    actions_in_wallet = False
    for macd_rec, signal_rec, price, date in zip(macd, signal, prices, dates):
        if not actions_in_wallet and macd_rec < signal_rec:
            wallet = wallet.buy_signal(price)
            story_of_trades.append(("Buy", price, wallet.money, wallet.number_of_actions, date))
            actions_in_wallet = True

        if actions_in_wallet and macd_rec > signal_rec:
            wallet = wallet.sell_signal(price)
            story_of_trades.append(("Sale", price, wallet.money, wallet.number_of_actions, date))
            money_story.append((date, wallet.money))
            actions_in_wallet = False

    for trade in story_of_trades[1:]:
        print("Money after trade: ", trade[2])
        print("Stocks after trade: ", trade[3])
        print("Date: ", trade[4])

    macds = [macd[0] for macd in macd_and_dates]
    macddate = [macd[1] for macd in macd_and_dates]
    signals = [signal[0] for signal in signal_and_dates]
    signaldate = [signal[1] for signal in signal_and_dates]
    plt.plot(macddate, macds, color="blue", label="MACD")
    plt.plot(signaldate, signals, color="orange", label="Signal")
    plt.legend()
    plt.xticks(rotation=45, fontsize=8)
    ax = plt.gca()
    temp = ax.xaxis.get_ticklabels()
    temp = list(set(temp) - set(temp[::30]))
    for label in temp:
        label.set_visible(False)
    plt.title('WIG 20')
    plt.tight_layout()

    sell_dates = [trade[4] for trade in story_of_trades if trade[0] == "Sale"]
    macd_and_dates_d = {}
    for tup in macd_and_dates:
        macd_and_dates_d[tup[1]] = tup[0]
    sell_macd = [macd_and_dates_d.get(sell_date) for sell_date in sell_dates]
    plt.scatter(sell_dates, sell_macd, color='red', label='Sell')

    buy_dates = [trade[4] for trade in story_of_trades if trade[0] == "Buy"]
    macd_and_dates_d = {}
    for tup in macd_and_dates:
        macd_and_dates_d[tup[1]] = tup[0]
    buy_macd = [macd_and_dates_d.get(buy_date) for buy_date in buy_dates]
    # plt.scatter(buy_dates, buy_macd, color='green', label='Buy')
    # plt.savefig(fname="macdsignalwig20.jpg", dpi=200)
    # plt.show()

    buy_date_values = [data_dict.get(data) for data in buy_dates]
    plt.scatter(buy_dates, buy_date_values)
    plt.plot(dates, [data_dict.get(data) for data in dates])
    plt.show()


    # Rysowanie wykresu z datami transakcji na osi x
    dates, money = zip(*money_story)
    plt.plot(dates, money)
    plt.xlabel('Date of Transaction')
    plt.ylabel('Money')
    plt.title('Money Over Time')
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()
    plt.show()
