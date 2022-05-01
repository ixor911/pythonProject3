import time


class Candle:
    def __init__(self, rough_candle=None, head=0, body=0, tail=0, direction=None):
        if rough_candle is None:
            rough_candle = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

        self.time = float(rough_candle[0])
        self.start = float(rough_candle[1])
        self.end = float(rough_candle[4])
        self.max = float(rough_candle[2])
        self.min = float(rough_candle[3])
        self.tbq = float(rough_candle[10])

        self.head = head
        self.body = body
        self.tail = tail
        if direction is None:
            if self.start <= self.end:
                self.direction = 1
            else:
                self.direction = -1
        else:
            self.direction = direction

        if (head == 0) & (body == 0) & (tail == 0):
            try:
                full_length = self.max - self.min
                self.body = (self.end - self.start) * self.direction / full_length
                if self.direction == 1:
                    self.head = (self.max - self.end) / full_length
                    self.tail = (self.start - self.min) / full_length
                else:
                    self.head = (self.max - self.start) / full_length
                    self.tail = (self.end - self.min) / full_length
            except:
                self.head = 0
                self.body = 0
                self.tail = 0


class Pattern:
    def __init__(self, name, pattern_combo, error, amount_candles, candles_sizes):
        self.name = name
        self.pattern_combo = pattern_combo
        self.error = error
        self.amount_candles = amount_candles
        self.candles_sizes = candles_sizes

    def get_candles_sizes(self, candles_combo):
        max_value = 0
        min_value = 99999999999
        candles_sizes = []

        for candle in candles_combo:
            if candle.max > max_value:
                max_value = candle.max

            if candle.min < min_value:
                min_value = candle.min

        dif = max_value - min_value
        for candle in candles_combo:
            c_dif = candle.max - candle.min
            try:
                candles_sizes.append(round(c_dif / dif, 2))
            except:
                candles_sizes.append(0)

        return candles_sizes

    def compare_candle(self, pattern_candle, pattern_candle_size, error, new_candle, new_candle_size):
        check = [False, False, False, False]

        if (pattern_candle.head + error.get('head_top') > new_candle.head) & \
                (pattern_candle.head - error.get('head_bot') < new_candle.head):
            check[0] = True

        if (pattern_candle.body + error.get('body_top') > new_candle.body) & \
                (pattern_candle.body - error.get('body_bot') < new_candle.body):
            check[1] = True

        if (pattern_candle.tail + error.get('tail_top') > new_candle.tail) & \
                (pattern_candle.tail - error.get('tail_bot') < new_candle.tail):
            check[2] = True

        if pattern_candle.direction == new_candle.direction:
            check[3] = True

        # if (pattern_candle_size + error.get('size_top') > new_candle_size) & \
        #        (pattern_candle_size - error.get('size_bot') < new_candle_size):
        #    check[4] = True
        # print(check)

        try:
            if check.index(False) != -1:
                return False
        except:
            return True

    def compare_candles_combo(self, new_combo):
        start_index = len(new_combo) - len(self.pattern_combo)
        need_combo = []

        for need_index in range(0, len(self.pattern_combo) - 1):
            need_combo.append(new_combo[need_index + start_index])

        new_combo_sizes = self.get_candles_sizes(need_combo)
        check_combo = []

        for index in range(0, len(self.pattern_combo) - 1):
            pattern_candle = self.pattern_combo[index]
            error = self.error.get(index)
            # pattern_candle_size = self.candles_sizes[index]
            pattern_candle_size = []
            new_candle = new_combo[index + start_index]
            new_candle_size = new_combo_sizes[index]

            check_combo.append(self.compare_candle(pattern_candle, pattern_candle_size, error, new_candle,
                                                   new_candle_size))

        try:
            if check_combo.index(False) != -1:
                return False
        except:
            return True


class Wallet:
    def __init__(self, cryptos, main_coin):
        self.cryptos = cryptos
        self.list_wallet_coins = {}
        self.main_coin = {
            'name': main_coin,
            'amount': 0.,
        }

        for coin in cryptos:
            self.list_wallet_coins[coin] = {
                'amount': 0.,
                'last_price': 0.,
                'filters': {}
            }

    def wallet_get_coin(self, coin):
        coin_info = {}
        if coin in self.cryptos:
            coin_in_wallet = self.list_wallet_coins.get(coin)
            coin_info = {
                'name': coin,
                'amount': coin_in_wallet.get('amount'),
                'last_price': coin_in_wallet.get('last_price'),
                'filters': coin_in_wallet.get('filters')
            }
        return coin_info

    def set_coins_filters(self, client):
        for coin in self.cryptos:
            symbol = f"{coin}{self.main_coin.get('name')}"
            symbol_info = client.get_symbol_info(symbol)
            symbol_filters = symbol_info.get('filters')

            for s_filter in symbol_filters:
                self.list_wallet_coins.get(coin).get('filters')[s_filter.get('filterType')] = s_filter

    def set_coin_value(self, spot, client, coin):
        self.list_wallet_coins.get(coin)['amount'] = float(client.get_asset_balance(asset=coin).get('free'))

        try:
            symbol = f"{coin}{self.main_coin.get('name')}"
            last_traid = spot.my_trades(symbol, limit=1)[0]
            self.list_wallet_coins.get(coin)['last_price'] = float(last_traid.get('price'))
        except:
            self.list_wallet_coins.get(coin)['last_price'] = 0.

    def set_main_coin_value(self, client):
        self.main_coin['amount'] = float(client.get_asset_balance(asset=self.main_coin.get('name')).get('free'))

    def set_coins_values(self, spot, client):
        for coin in self.cryptos:
            # self.set_coin_value(spot, client, coin)
            self.list_wallet_coins.get(coin)['amount'] = 0.

        # self.set_main_coin_value(client)
        self.main_coin['amount'] = 1000.


def sell_coin(spot, client, wallet, coin, new_candle_end, coef=0.):
    amount_coin = wallet.wallet_get_coin(coin).get('amount')
    filters = wallet.wallet_get_coin(coin).get('filters')

    amount_sell_coin = amount_coin
    amount_sell_coin = my_round(amount_sell_coin, float(filters.get('LOT_SIZE').get('minQty')))

    min_notional = float(filters.get('MIN_NOTIONAL').get('minNotional'))

    if amount_sell_coin <= 0:
        # print(f"не получилось продать {coin} 100")
        return 100
    # print(f"{new_candle_end * amount_sell_coin} <= {min_notional}")
    if new_candle_end * amount_sell_coin <= min_notional:
        # print(f"не получилось продать {coin} 101")
        return 101

    wallet.list_wallet_coins.get(coin)['amount'] -= amount_sell_coin
    wallet.main_coin['amount'] += amount_sell_coin * new_candle_end * 0.999

    return 1


def analyze_sma0(spot, client, wallet, coin, new_candles_combo, is_buy, coef):
    sma_5 = find_sma(new_candles_combo, 5)
    sma_15 = find_sma(new_candles_combo, 21)
    sma_45 = find_sma(new_candles_combo, 60)

    last_candle = new_candles_combo[len(new_candles_combo) - 1]



    #if (is_buy == True) & (sma_5 > sma_15) * (sma_15 > sma_45):
    #    log = buy_coin(spot, client, wallet, coin, last_candle, coef)
    #    return sma_5, sma_15, sma_45, log
    #elif (is_buy == False) & (sma_5 < sma_15 * 1.0):
    #    log = sell_coin(spot, client, wallet, coin, last_candle.end, coef)
    #    return sma_5, sma_15, sma_45, log

    return sma_5, sma_15, sma_45, 0


def buy_coin(spot, client, wallet, coin, new_candle, coef=0., amount=0.):
    amount_main_coin = wallet.main_coin.get('amount')
    filters = wallet.list_wallet_coins.get(coin).get('filters')

    amount_buy = amount_main_coin * coef
    amount_buy = my_round(amount_buy, float(filters.get('LOT_SIZE').get('minQty')))
    amount_buy_coin = new_candle.end * amount_buy

    min_notional = float(filters.get('MIN_NOTIONAL').get('minNotional'))
    min_lot_size = float(filters.get('LOT_SIZE').get('minQty'))

    # print(f"{amount_buy} <= {min_notional}")
    if amount_buy <= min_notional:
        # print(f"не получилось купить {coin} по цене:{new_candle_end} ||||100")
        return 100

    # print(f"{amount_buy_coin} <= {min_lot_size}")
    # if amount_buy_coin <= min_lot_size:
    #    print(f"не получилось купить {coin} 102")
    #    return

    # try:
    #    spot.new_order(f"{coin}{wallet.main_coin.get('name')}", "BUY", "MARKET", quoteOrderQty=amount_buy)
    # except:
    #    print(f"не получилось купить {coin} 101")
    #    return 101

    # wallet.set_coin_value(spot, client, coin)
    # wallet.set_main_coin_value(client)

    wallet.main_coin['amount'] -= amount_buy
    wallet.list_wallet_coins.get(coin)['amount'] += amount_buy / new_candle.end * 0.999
    wallet.list_wallet_coins.get(coin)['last_price'] = new_candle.end

    return 1


def my_round(number, coef):
    counter = 0
    counter_helper = coef
    while counter_helper < 1:
        counter += 1
        counter_helper *= 10
    return round(number - (number % coef), counter)


def find_sma(candles_combo, sma_coef):
    sma_coef -= 1
    last_index = len(candles_combo) - 1
    if last_index < sma_coef - 1:
        print("Ошибка в функции find_sma 101")
        return 0

    start_index = last_index - sma_coef

    sum = 0
    for index in range(start_index, last_index + 1):
        sum += candles_combo[index].end

    return sum / (sma_coef + 1)


def sma(candles_combo):
    last_index = len(candles_combo) - 1
    start_index_5 = last_index - 4

    sum5 = 0
    for index in range(start_index_5, last_index + 1):
        sum5 += candles_combo[index]
        print(sum5)
    sum5 /= 5

    start_index_15 = last_index - 14
    print()
    sum15 = 0
    for index in range(start_index_15, last_index + 1):
        sum15 += candles_combo[index]
        print(sum15)
    sum15 /= 15

    print(f"{sum5} < {sum15}")
    if sum5 > sum15:
        print("------------------------------------------------------------------------------------------------------")
        time.sleep(99999)

