import asyncio
from time import time
from typing import Optional, Dict, Tuple, Any, List

import aiohttp

from binance_config import DELETE_ZEROS, PUMP_PERCENT, SELL_ZONE_PERCENTS, PERCENT_TO_NOT_DELETE_POST, \
    PERCENT_TO_RETURN_CRYPT_TO_PULL, TIME_TO_NOT_DELETE_POST
from . import TGPublisher
from database import Database
from database.models import CoinModel

URL = 'https://api.binance.com/api/v3/klines?symbol='


class ParserModule:
    """
    Responsible for the entire process of working with binance.
    Receives information about coins and processes it depending on the state of crumples.
    """

    async def init_parsing(self) -> None:
        """
        Create task to run parsing

        :return:
        :rtype:
        """
        asyncio.create_task(self.parse_binance())

    async def get_coin_info(self, session: aiohttp.ClientSession, symbol: str) -> Optional[Tuple[str, Any]]:
        """
        Makes aiohttp request to binance for information about a coin pair

        :param session: aiohttp session
        :type session: ClientSession
        :param symbol: symbol of coins pair
        :type symbol: str
        :return: coin pair information
                if request was successful
        :rtype: Optional[Dict]
        """
        url = URL + f'{symbol}&limit=2&interval=1m'
        async with session.get(url) as resp:
            info = (await resp.json())[0]
            return symbol, info

    async def parse_binance(self):
        """
        Opens aiohttp session and collects information about all coin pairs

        :return:
        :rtype:
        """
        coins = Database.get_coins()

        if coins:
            async with aiohttp.ClientSession() as session:

                tasks = []
                for coin in coins:
                    tasks.append(asyncio.ensure_future(self.get_coin_info(session, coin.symbol)))

                all_coins_info = await asyncio.gather(*tasks, return_exceptions=True)
                for symbol, info in all_coins_info:
                    print(symbol, info)
                    continue
                    coin = await Database.get_coin(symbol)

                    if coin.status == 'treated':
                        await self.process_treated_coin(coin, info)

                    elif coin.status == 'untreated':
                        await self.process_untreated_coin(coin, info)

                    else:
                        raise ZeroDivisionError

        print('Finish')

    async def process_treated_coin(self, coin: CoinModel, data: List[Any]):
        """

        :param coin:
        :type coin:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        symbol = coin.symbol

        old_price = coin.price / DELETE_ZEROS
        new_price = float(data[4])
        percent = self.get_percent(old_price, new_price)

        timestamp = coin.timestamp
        time_now = time()

        try:
            if coin.post and coin.post.to_delete \
                    and time_now - timestamp > TIME_TO_NOT_DELETE_POST and percent < PERCENT_TO_NOT_DELETE_POST:
                post_id = coin.post.post_id
                await TGPublisher.delete_post(post_id)

        except Exception as e:
            print(e)

        try:
            if coin.post and coin.post.to_delete \
                    and time_now - timestamp <= TIME_TO_NOT_DELETE_POST and percent >= PERCENT_TO_NOT_DELETE_POST:
                post_id = coin.post.post_id
                if await Database.change_post_status(post_id):
                    print(f'Post with id {post_id} was successfully marked as completed')

        except Exception as e:
            print(e)

        try:
            entered_targets = coin.entered_targets
            open_target = coin.open_target

            post_id = coin.post.post_id if coin.post else None

            await self.check_entered_targets(symbol=symbol, entered_targets=entered_targets, timestamp=timestamp,
                                             percent=percent, post_id=post_id, open_target=open_target)

        except Exception as e:
            print(e)

    async def process_untreated_coin(self, coin: CoinModel, data: List[Any]):
        """

        :param coin:
        :type coin: database.models.coin_model.CoinModel
        :param data:
        :type data: List[Any]
        :return:
        :rtype: None
        """
        old_price = float(data[1])
        new_price = float(data[2])

        timestamp = int(data[0] / 1000)

        if coin.last_timestamp is None:
            coin = await Database.write_last_data(coin.symbol, new_price, timestamp)

        percent = self.get_percent(old_price, new_price)

        if percent >= PUMP_PERCENT:
            await self.create_pump_post(coin.symbol, new_price, timestamp)

        else:
            time_now = int(time())

            if time_now - coin.last_timestamp >= 15 * 60:
                print('Change 15 minutes price')
                await Database.write_last_data(coin.symbol, new_price, timestamp)

            else:
                last_price = coin.last_price / DELETE_ZEROS

                percent = self.get_percent(last_price, new_price)
                if percent >= PUMP_PERCENT:
                    await self.create_pump_post(coin.symbol, new_price, timestamp)

    async def create_pump_post(self, symbol: str, price: float, timestamp: int):
        """

        :param symbol:
        :type symbol: str
        :param price:
        :type price: float
        :param timestamp:
        :type timestamp: int
        :return:
        :rtype:
        """
        await TGPublisher.create_pump_post(symbol, price, timestamp)

    async def check_entered_targets(self, symbol: str, timestamp: int, entered_targets: List[int], open_target: int,
                                    percent: float, post_id: Optional[int]):
        """

        :param symbol:
        :type symbol: str
        :param timestamp:
        :type timestamp: int
        :param entered_targets:
        :type entered_targets: List[int]
        :param open_target:
        :type open_target: int
        :param percent:
        :type percent: float
        :param post_id:
        :type post_id: Optional[int]
        :return:
        :rtype:
        """
        print(f'--> Check targets for coin {symbol} {percent}')
        target_list = list(set(SELL_ZONE_PERCENTS) - set(entered_targets))

        print(f'Target list {target_list=}')

        t = int(time() - timestamp - 10)

        for target in target_list:
            if percent >= target:
                if Database.add_target(symbol=symbol, target=target) and post_id:
                    period = self.get_period(seconds=t)
                    symbol = f'#{symbol[:-3]}'

                    if Database.write_daily_statistic(symbol=symbol, percent=percent, period=period):
                        target_index = SELL_ZONE_PERCENTS.index(target) + 1

                        symbol = symbol[1:]
                        await TGPublisher.create_target_enter_post(symbol=symbol, target_index=target_index,
                                                                   seconds=t, period=period, percent=percent,
                                                                   post_id=post_id, open_target=open_target)

        print(f'Check targets for coin {symbol} {percent} --> ')

        try:
            if percent >= PERCENT_TO_RETURN_CRYPT_TO_PULL:
                print(f'--> Return coin {symbol} to pool')
                if await Database.return_coin_to_pool(symbol):
                    print(f'Coin {symbol} was successfully returned to pool')

            print(f'Return coin {symbol} to pool --> ')

        except Exception as e:
            print(e)

    def get_percent(self, old_price: float, new_price: float):
        """

        :param old_price:
        :type old_price: float
        :param new_price:
        :type new_price: float
        :return:
        :rtype: float
        """
        percent = round(new_price * 100 / old_price - 100, 2)
        return percent

    def get_period(self, seconds: int):
        """

        :param seconds:
        :type seconds:
        :return:
        :rtype:
        """
        days = int(seconds / (3600 * 24))
        rem = seconds % (3600 * 24)
        hours = int(rem / 3600)
        rem = rem % 3600
        minutes = int(rem / 60)

        if days == 0 and hours == 0:
            return f"{minutes} Minutes"
        elif days == 0:
            return f"{hours} Hours {minutes} Minutes"
        else:
            return f"{days} Days {hours} Hours {minutes} Minutes"
