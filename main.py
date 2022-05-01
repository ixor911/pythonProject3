import time

from binance.spot import Spot
from binance.client import Client
from binance import ThreadedWebsocketManager
from binance_ixor import *
import matplotlib.pyplot as plt
import numpy as np

api_key = "4bRqCMlCkjxLoIfAT6NBwFHG15VtbmJ1WtI1JZgb0E3tfRasJjSPi12icZotddV5"
secret_key = "WYnoEo1mIhAQWqzpXSqAEXVeEXsVSv3iQc08yACFUAuCrh7vRGwgpYzwy50UHeCl"
spot = Spot(api_key, secret_key)
client = Client(api_key, secret_key)

# -----------------------------------------------------------------------------------------

#cryptos = ["BTC", "ETH", "XRP", "ETC", "BNB", "SOL", "ADA", "LUNA", "AVAX",
#           "DOGE", "DOT", "UST", "SHIB", "MATIC", "NEAR", "BUSD",
#           "LTC", "UNI", "BCH", "LINK", "TRX", "FTT"]
cryptos = ["XRP"]
main_coin = "USDT"

wallet = Wallet(cryptos, "USDT")
wallet.set_coins_filters(client)
wallet.set_coins_values(spot, client)
# -----------------------------------------------------------------------------------------
print("start")
# rough_candles = spot.klines(f"{coin}{wallet.main_coin.get('name')}", interval="5m", limit=5)
# 5m = 300000ms
# 1h = 12 * 5m = 3600000ms
# 1d = 24h = 228 * 5m = 86400000ms
# 10d = 240h = 2280 * 5m = 864000000ms
m5 = 300000
h1 = m5 * 12
d1 = h1 * 24
d10 = d1 * 10

amount_sell_10d = 0
sell_coefs = []
sell_types = [0, 0]
sell_errors = [0, 0]

buy_errors = [0]

start_money = 1000.

start_time = spot.time().get('serverTime') - 2000 * h1 - d1
all_candles = {}
for coin in cryptos:
    all_candles[coin] = []

    rough_candles = spot.klines(f"{coin}{main_coin}", interval="1h", limit=1000, startTime=start_time)
    for candle in rough_candles:
        all_candles[coin].append(Candle(candle))
    rough_candles = spot.klines(f"{coin}{main_coin}", interval="1h", limit=1000, startTime=start_time + 1000 * h1)
    for candle in rough_candles:
        all_candles[coin].append(Candle(candle))

all_candles_last_index = len(all_candles.get('XRP')) - 1
sma_arr = [[], [], [], [], []]
for last_index in range(65, all_candles_last_index):
    first_index = last_index - 65
    for coin in cryptos:
        new_candles = []
        for index in range(first_index, last_index):
            new_candles.append(all_candles[coin][index])

        # ---------------------------------- analyze function ----------------------------------------------------

        coin_amount = wallet.list_wallet_coins.get(coin).get('amount')
        main_coin_amount = wallet.main_coin.get('amount')

        min_notional = float(
            wallet.list_wallet_coins.get(coin).get('filters').get('MIN_NOTIONAL').get('minNotional'))

        last_candle_index = len(new_candles) - 1
        last_candle = new_candles[last_candle_index]

        new_sma_5, new_sma_15 = 0., 0.
        if coin_amount * last_candle.end <= min_notional:
            new_sma_5, new_sma_15, new_sma_45, buy_code = analyze_sma0(spot, client, wallet, coin, new_candles, True, 0.5)
            sma_arr[0].append(last_index)
            sma_arr[1].append(last_candle.end)
            sma_arr[2].append(new_sma_5)
            sma_arr[3].append(new_sma_15)
            sma_arr[4].append(new_sma_45)
            pass

        last_buy_price = wallet.wallet_get_coin(coin).get('last_price')
        sell_coef = 0.
        if coin_amount * last_candle.end > min_notional:
            new_sma_5, new_sma_15, new_sma_45, sell_code = analyze_sma0(spot, client, wallet, coin, new_candles, False, 1)
            sma_arr[0].append(last_index)
            sma_arr[1].append(last_candle.end)
            sma_arr[2].append(new_sma_5)
            sma_arr[3].append(new_sma_15)
            sma_arr[4].append(new_sma_45)

            if sell_code == 1:
                amount_sell_10d += 1
                if last_candle.end > last_buy_price:
                    sell_types[0] += 1
                else:
                    sell_types[1] += 1





# ------------------------------if still have coins----------------------------------------------
x = np.array(sma_arr[0])
y0 = np.array(sma_arr[1])
y1 = np.array(sma_arr[2])
y2 = np.array(sma_arr[3])
y3 = np.array(sma_arr[4])
plt.plot(x, y0)
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)

plt.show()


for coin in cryptos:
    coin_amount = wallet.wallet_get_coin(coin).get('amount')
    coin_last_price = wallet.wallet_get_coin(coin).get('last_price')
    min_notional = float(
        wallet.list_wallet_coins.get(coin).get('filters').get('MIN_NOTIONAL').get('minNotional'))
    min_lot_size = float(
        wallet.list_wallet_coins.get(coin).get('filters').get('LOT_SIZE').get('minQty'))

    coin_amount = my_round(coin_amount, min_lot_size)

    if coin_amount * coin_last_price > min_notional:
        wallet.main_coin['amount'] += coin_amount * coin_last_price

# ---------------------------------RESULTS---------------------------------------------------

amount_sell_1d = amount_sell_10d / 30
amount_sell_1h = amount_sell_1d / 24

end_money = round(wallet.main_coin.get('amount'), 1)
money_gain_coef = end_money / start_money

print(f"Всего продаж (10 дней): {amount_sell_10d}\n"
      f"Продаж за день (в среднем): {amount_sell_1d}\n"
      f"Продаж за час (в среднем): {amount_sell_1h}\n")

print(f"Кол-во хороших продаж: {sell_types[0]}\n"
      f"Кол-во плохих продаж: {sell_types[1]}\n")

print(f"Начальная сумма денег: {start_money}\n"
      f"Конечная сумма денег: {end_money}\n"
      f"Коеф роста: {money_gain_coef}\n")

#buy_err_sum = buy_errors[0]
#print(f"Кол-во ошибок покупок: {buy_err_sum}\n"
#          f"\t100: {buy_errors[0]}\n")

#sell_err_sum = sell_errors[0] + sell_errors[1]
#print(f"Кол-во ошибок продаж: {sell_err_sum}\n"
#          f"\t100: {sell_errors[0]}\n"
#          f"\t101: {sell_errors[1]}\n")



