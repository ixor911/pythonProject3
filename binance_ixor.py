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
                'last_time': 0,
                'last_pattern': 0.,
                'last_good_candle': Candle(),
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
                'last_time': coin_in_wallet.get('last_time'),
                'last_pattern': coin_in_wallet.get('last_pattern'),
                'last_good_candle': coin_in_wallet.get('last_good_candle'),
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

    # try:
    #    spot.new_order(f"{coin}{wallet.main_coin.get('name')}", "SELL", "MARKET", quantity=amount_sell_coin)
    # except:
    #    print(f"не получилось продать {coin} 102")
    #    return 102

    # wallet.set_coin_value(spot, client, coin)
    # wallet.set_main_coin_value(client)

    wallet.list_wallet_coins.get(coin)['amount'] -= amount_sell_coin
    wallet.main_coin['amount'] += amount_sell_coin * new_candle_end * 0.999

    return 1

    # last_trade = spot.my_trades(f"{coin}{wallet.main_coin.get('name')}", limit=1)[0]
    # print(f"продал {coin} - {amount_sell_coin}")
    # print(f"{last_trade}\n")


def analyze_sell0(spot, client, wallet, coin, new_candles_combo, coef=0.5):
    last_candle_index = len(new_candles_combo) - 1
    last_candle = new_candles_combo[last_candle_index]

    if (last_candle.end > wallet.wallet_get_coin(coin).get('last_price') * 1.02) | \
            (last_candle.end < wallet.wallet_get_coin(coin).get('last_price') * 0.98) | \
            (last_candle.tbq < 10):
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)
    return 0


def analyze_sell1(spot, client, wallet, coin, new_candles_combo, coef=0.5):
    last_candle_index = len(new_candles_combo) - 1
    last_candle = new_candles_combo[last_candle_index]
    buy_price = wallet.wallet_get_coin(coin).get('last_price')

    if last_candle.end < buy_price * 0.98:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    if last_candle.direction == 1:
        wallet.list_wallet_coins.get(coin)['last_good_candle'] = last_candle

    if last_candle.direction == -1:
        last_good_candle = wallet.wallet_get_coin(coin).get('last_good_candle')
        last_good_candle_size = last_good_candle.end - last_good_candle.start
        max_fall = last_good_candle.end - last_good_candle_size * coef

        if last_candle.end <= max_fall:
            return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    return 0


def analyze_sell2(spot, client, wallet, coin, new_candles_combo, amount_falls, coef=1):
    buy_price = wallet.wallet_get_coin(coin).get('last_price')
    last_index = len(new_candles_combo) - 1
    last_candle = new_candles_combo[last_index]

    if new_candles_combo[last_index].end < buy_price * coef:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    last_candles = []
    while last_index >= last_index - amount_falls:
        last_candles.append(new_candles_combo[last_index])

    candles_directions = []
    for candle in last_candles:
        candles_directions.append(candle.direction)

    try:
        if candles_directions.index(1) != -1:
            return 0
    except:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)


def analyze_sell3(spot, client, wallet, coin, new_candles_combo, coef=1):
    buy_price = wallet.wallet_get_coin(coin).get('last_price')
    buy_time = wallet.wallet_get_coin(coin).get('last_time')
    last_index = len(new_candles_combo) - 1
    last_candle = new_candles_combo[last_index]

    if new_candles_combo[last_index].end < buy_price * coef:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    if last_candle.time > buy_time * 1800000:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    return 0


def analyze_sell13(spot, client, wallet, coin, new_candles_combo, coef=1):
    last_candle_index = len(new_candles_combo) - 1
    last_candle = new_candles_combo[last_candle_index]
    buy_price = wallet.wallet_get_coin(coin).get('last_price')
    buy_time = wallet.wallet_get_coin(coin).get('last_time')

    if last_candle.end < buy_price * coef:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    if last_candle.time > buy_time * 1800000:
        return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    if last_candle.direction == -1:
        prev_index = last_candle_index - 1
        prev_direction = new_candles_combo[prev_index].direction

        while prev_direction != 1:
            prev_index -= 1
            prev_direction = new_candles_combo[prev_index]

        prev_candle = new_candles_combo[prev_index]
        prev_size = prev_candle.end - prev_candle.start
        max_fall = prev_candle.end - prev_size * coef

        if last_candle.end <= max_fall:
            return sell_coin(spot, client, wallet, coin, last_candle.end, 1)

    return 0


def analyze_sma0(spot, client, wallet, coin, new_candles_combo, is_buy, coef):
    sma_5 = find_sma(new_candles_combo, 5)
    sma_15 = find_sma(new_candles_combo, 15)
    last_candle = new_candles_combo[len(new_candles_combo) - 1]

    if (is_buy == True) & (sma_5 > sma_15):
        return buy_coin(spot, client, wallet, coin, last_candle, 3, coef)
    elif (is_buy == False) & (sma_5 < sma_15):
        return sell_coin(spot, client, wallet, coin, last_candle.end, coef)

    return 0


def buy_coin(spot, client, wallet, coin, new_candle, pattern_used, coef=0., amount=0.):
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
    wallet.list_wallet_coins.get(coin)['last_time'] = new_candle.time
    wallet.list_wallet_coins.get(coin)['last_pattern'] = pattern_used
    wallet.list_wallet_coins.get(coin)['last_good_candle'] = new_candle

    return 1

    # last_trade = spot.my_trades(f"{coin}{wallet.main_coin.get('name')}", limit=1)[0]
    # print(f"купил {coin} за {amount_buy}")
    # print(f"{last_trade}\n")


def analyze(spot, client, wallet, buy_patterns, new_candle_combo, coin):
    coin_amount = wallet.list_wallet_coins.get(coin).get('amount')
    main_coin_amount = wallet.main_coin.get('amount')

    min_notional = float(wallet.list_wallet_coins.get(coin).get('filters').get('MIN_NOTIONAL').get('minNotional'))

    last_index = len(new_candle_combo) - 1
    last_candle = new_candle_combo[last_index]
    if coin_amount * last_candle.end <= min_notional:
        for pattern in buy_patterns:
            if pattern.compare_candles_combo(new_candle_combo):
                print(buy_patterns.index(pattern))
                buy_coin(spot, client, wallet, coin, last_candle.end, 0.5)
                return
        return

    if (wallet.wallet_get_coin(coin).get('last_price') * 1.02 <= last_candle.end) | \
            (wallet.wallet_get_coin(coin).get('last_price') * 0.98 > last_candle.end):
        sell_coin(spot, client, wallet, coin, last_candle.end, 1)


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
    if last_index < sma_coef:
        print("Ошибка в функции find_sma 101")
        return 0

    start_index = last_index - sma_coef

    sum = 0
    for index in range(start_index, last_index):
        sum += candles_combo[index].end

    return sum / (sma_coef + 1)


def sma(candles_combo):
    last_index = len(candles_combo) - 1
    start_index_5 = last_index - 4

    sum5 = 0
    for index in range(start_index_5, last_index):
        sum5 += candles_combo[index].end
    sum5 /= 5

    start_index_15 = last_index - 14

    sum15 = 0
    for index in range(start_index_15, last_index):
        sum15 += candles_combo[index].end
    sum15 /= 15

    print(f"{sum5} < {sum15}")
    if sum5 > sum15:
        print("------------------------------------------------------------------------------------------------------")
        time.sleep(99999)

