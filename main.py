import time

from binance.spot import Spot
from binance.client import Client
from binance import ThreadedWebsocketManager
from binance_ixor import *

api_key = "4bRqCMlCkjxLoIfAT6NBwFHG15VtbmJ1WtI1JZgb0E3tfRasJjSPi12icZotddV5"
secret_key = "WYnoEo1mIhAQWqzpXSqAEXVeEXsVSv3iQc08yACFUAuCrh7vRGwgpYzwy50UHeCl"
spot = Spot(api_key, secret_key)
client = Client(api_key, secret_key)


# d1_timer = start_time
# while d1_timer <= start_time + d10:
#    h1_timer = d1_timer + h1
#    while h1_timer <= d1_timer + d1:
#        m5_timer = h1_timer + m5
#        while m5_timer <= h1_timer + h1:
#
#
#            m5_timer += m5
#        h1_timer += h1
#    d1_timer += d1

buy_hammer_combo = [
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0., body=0.30, tail=0.70, direction=1)
    #Candle(head=0.16, body=0.67, tail=0.16, direction=1)
]
buy_hammer_sizes = [0.31, 0.31, 0.31, 0.38, 0.31]
buy_hammer_errors = {
    0: {
        'head_top': 0.1,
        'head_bot': 0.1,
        'body_top': 0.1,
        'body_bot': 0.1,
        'tail_top': 0.1,
        'tail_bot': 0.1,
        'size_top': 0.1,
        'size_bot': 0.1
    },
    1: {
        'head_top': 0.1,
        'head_bot': 0.1,
        'body_top': 0.1,
        'body_bot': 0.1,
        'tail_top': 0.1,
        'tail_bot': 0.1,
        'size_top': 0.1,
        'size_bot': 0.1
    },
    2: {
        'head_top': 0.03,
        'head_bot': 0.03,
        'body_top': 0.03,
        'body_bot': 0.03,
        'tail_top': 0.03,
        'tail_bot': 0.03,
        'size_top': 0.03,
        'size_bot': 0.03
    },



}
buy_hammer = Pattern(0, buy_hammer_combo, buy_hammer_errors, 3, buy_hammer_sizes)
# --------------------------------------------------------------------------------------------------------

buy_reverse_hammer_combo = [
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.83, body=0.16, tail=0., direction=-1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=1)
]
buy_reverse_hammer_sizes = [0.3, 0.3, 0.45, 0.48]
buy_reverse_hammer_errors = {
    0: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    },
    1: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    },
    2: {
        'head_top': 0.00,
        'head_bot': 0.00,
        'body_top': 0.00,
        'body_bot': 0.00,
        'tail_top': 0.00,
        'tail_bot': 0.00,
        'size_top': 0.00,
        'size_bot': 0.00
    },
    3: {
        'head_top': 0.00,
        'head_bot': 0.00,
        'body_top': 0.00,
        'body_bot': 0.00,
        'tail_top': 0.00,
        'tail_bot': 0.00,
        'size_top': 0.00,
        'size_bot': 0.00
    },
    4: {
        'head_top': 0.00,
        'head_bot': 0.00,
        'body_top': 0.00,
        'body_bot': 0.00,
        'tail_top': 0.00,
        'tail_bot': 0.00,
        'size_top': 0.00,
        'size_bot': 0.00
    }

}

buy_reverse_hammer = Pattern(1, buy_reverse_hammer_combo, buy_reverse_hammer_errors, 5, buy_reverse_hammer_sizes)
# ------------------------------------------------------------------------------------------------------------------
buy_smt_combo = [
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=-1),
    Candle(head=0.46, body=0.08, tail=0.46, direction=1),
    Candle(head=0.16, body=0.67, tail=0.16, direction=1)
]
buy_smt_sizes = [0.3, 0.3, 0.3]
buy_smt_errors = {
    0: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    },
    1: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    },
    2: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    },
    3: {
        'head_top': 0.0,
        'head_bot': 0.0,
        'body_top': 0.0,
        'body_bot': 0.0,
        'tail_top': 0.0,
        'tail_bot': 0.0,
        'size_top': 0.0,
        'size_bot': 0.0
    }
}

buy_smt_hammer = Pattern(2, buy_smt_combo, buy_smt_errors, 4, buy_smt_sizes)

# -------------------------------------------------------------------------------------------------------------------
buy_patterns = [buy_hammer, buy_reverse_hammer, buy_smt_hammer]
# -----------------------------------------------------------------------------------------

cryptos = ["BTC", "ETH", "XRP", "ETC", "BNB", "SOL", "ADA", "LUNA", "AVAX",
           "DOGE", "DOT", "UST", "SHIB", "MATIC", "NEAR", "BUSD",
           "LTC", "UNI", "BCH", "LINK", "TRX", "FTT"]
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

patterns_used = [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0]]]

start_time = spot.time().get('serverTime') - d10 - d1
all_candles = {}
for coin in cryptos:
    all_candles[coin] = []

    rough_candles = spot.klines(f"{coin}{main_coin}", interval="5m", limit=1000, startTime=start_time)
    for candle in rough_candles:
        all_candles[coin].append(Candle(candle))

    rough_candles = spot.klines(f"{coin}{main_coin}", interval="5m", limit=1000, startTime=start_time + m5 * 1000)
    for candle in rough_candles:
        all_candles[coin].append(Candle(candle))

    rough_candles = spot.klines(f"{coin}{main_coin}", interval="5m", limit=880, startTime=start_time + m5 * 2000)
    for candle in rough_candles:
        all_candles[coin].append(Candle(candle))


all_candles_last_index = len(all_candles.get('BTC')) - 1
for last_index in range(17, all_candles_last_index):
    first_index = last_index - 17
    for coin in cryptos:
        new_candles = []
        for index in range(first_index, last_index):
            new_candles.append(all_candles[coin][index])

        sma(new_candles)

        # ---------------------------------- analyze function ----------------------------------------------------

        coin_amount = wallet.list_wallet_coins.get(coin).get('amount')
        main_coin_amount = wallet.main_coin.get('amount')

        min_notional = float(
            wallet.list_wallet_coins.get(coin).get('filters').get('MIN_NOTIONAL').get('minNotional'))

        last_candle_index = len(new_candles) - 1
        last_candle = new_candles[last_candle_index]

        if coin_amount * last_candle.end <= min_notional:
            analyze_sma0(spot, client, wallet, coin, new_candles, True, 0.5)
            pass

        last_buy_price = wallet.wallet_get_coin(coin).get('last_price')
        sell_coef = 0.
        if coin_amount * last_candle.end > min_notional:
            sell_code = analyze_sma0(spot, client, wallet, coin, new_candles, False, 1)

            if sell_code == 1:
                sell_coef = last_candle.end / last_buy_price
                sell_coefs.append(sell_coef)

                pattern_used = wallet.wallet_get_coin(coin).get('last_pattern')

                if last_buy_price < last_candle.end:
                    sell_types[0] += 1
                    patterns_used[pattern_used][1][0] += 1
                else:
                    sell_types[1] += 1
                    patterns_used[pattern_used][1][1] += 1

                amount_sell_10d += 1
            elif sell_code != 0:
                sell_errors[sell_code - 100] += 1


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


# i = start_time
# while i <= start_time + d10:
#    k = i
#    while k <= i + h1:
#        for coin in cryptos:
#            rough_candles = spot.klines(f"{coin}{main_coin}", interval="5m", limit=5, startTime=k)
#            new_candle_combo = []
#            for index in range(0, 4):
#                new_candle_combo.append(Candle(rough_candles[index]))
#
#            # ---------------------------------- analyze function ----------------------------------------------------
#
#            coin_amount = wallet.list_wallet_coins.get(coin).get('amount')
#            main_coin_amount = wallet.main_coin.get('amount')
#
#            min_notional = float(
#                wallet.list_wallet_coins.get(coin).get('filters').get('MIN_NOTIONAL').get('minNotional'))
#
#            last_index = len(new_candle_combo) - 1
#            last_candle = new_candle_combo[last_index]
#
#            if coin_amount * last_candle.end <= min_notional:
#                for pattern in buy_patterns:
#                    if pattern.compare_candles_combo(new_candle_combo):
#                        patterns_used[pattern.name][0][0] += 1
#                        buy_code = buy_coin(spot, client, wallet, coin, last_candle.end, pattern.name, 0.5)
#
#                        if buy_code != 1:
#                            buy_errors[buy_code - 100] += 1
#                            patterns_used[pattern.name][0][1] += 1
#
#                        break
#                pass
#
#            last_buy_price = wallet.wallet_get_coin(coin).get('last_price')
#            sell_coef = 0.
#            if (last_buy_price * 1.02 <= last_candle.end) | (last_buy_price * 0.98 > last_candle.end):
#               sell_code = sell_coin(spot, client, wallet, coin, last_candle.end, 1)
#
#                if sell_code == 1:
#                    sell_coef = last_candle.end / last_buy_price
#                    sell_coefs.append(sell_coef)
#
#                    pattern_used = wallet.wallet_get_coin(coin).get('last_pattern')
#
#                    if last_buy_price < last_candle.end:
#                        sell_types[0] += 1
#                        patterns_used[pattern_used][1][0] += 1
#                    else:
#                        sell_types[1] += 1
#                        patterns_used[pattern_used][1][1] += 1
#
#                    amount_sell_10d += 1
#                else:
#                    sell_errors[sell_code - 100] += 1
#
#        k += m5
#    i += d1


amount_sell_1d = amount_sell_10d / 10
amount_sell_1h = amount_sell_10d / 240

mid_sell_coef = 0
for coef in sell_coefs:
    mid_sell_coef += coef

try:
    mid_sell_coef /= len(sell_coefs)
except:
    mid_sell_coef = 0

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

print(f"Средний коеф роста: {mid_sell_coef}\n")

print(f"Использовались шаблоны:\n"
        f"\t'Молот': {patterns_used[0][0][0]}\n"
            f"\t\tУдачно: {patterns_used[0][0][0] - patterns_used[0][0][1]}\n"
            f"\t\tНеудачно: {patterns_used[0][0][1]}\n"
        f"\t'Реверсивный молот': {patterns_used[1][0][0]}\n"
              f"\t\tУдачно: {patterns_used[1][0][0] - patterns_used[1][0][1]}\n"
              f"\t\tНеудачно: {patterns_used[1][0][1]}\n"
        f"\t'Волчек': {patterns_used[2][0][0]}\n"
              f"\t\tУдачно: {patterns_used[2][0][0] - patterns_used[2][0][1]}\n"
              f"\t\tНеудачно: {patterns_used[2][0][1]}\n"
      )

print(f"Удачность продаж по шаблонам:\n"
        f"\t'Молот':\n"
            f"\t\tУдачно: {patterns_used[0][1][0]}\n"
            f"\t\tНеудачно: {patterns_used[0][1][1]}\n"
        f"\t'Реверсивный молот':\n"
              f"\t\tУдачно: {patterns_used[1][1][0]}\n"
              f"\t\tНеудачно: {patterns_used[1][1][1]}\n"
        f"\t'Волчек':\n"
              f"\t\tУдачно: {patterns_used[2][1][0]}\n"
              f"\t\tНеудачно: {patterns_used[2][1][1]}\n"
      )

buy_err_sum = buy_errors[0]
print(f"Кол-во ошибок покупок: {buy_err_sum}\n"
          f"\t100: {buy_errors[0]}\n")

sell_err_sum = sell_errors[0] + sell_errors[1]
print(f"Кол-во ошибок продаж: {sell_err_sum}\n"
          f"\t100: {sell_errors[0]}\n"
          f"\t101: {sell_errors[1]}\n")



