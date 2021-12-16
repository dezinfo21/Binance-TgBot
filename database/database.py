from calendar import monthrange
from datetime import datetime, timedelta
from random import randint
from time import time
from typing import List, Optional, Dict, Any

import certifi
from mongoengine import connect
from mongoengine import ConnectionFailure

from binance import Client

from binance_config import DELETE_ZEROS
from .models import CoinModel, PostModel, IGPostModel
from .models.daily_coin_statistic_model import DailyCoinStatisticModel


class Database:
    """
    Database class controls access to the database.
    Implements all commands for data access.
    """

    # -- CONNECTION --

    @staticmethod
    def connect(db_uri: str) -> None:
        """
        Connection method.
        Exit program if connection has failed.

        :param db_uri: database connection string
        :type db_uri: str
        :return:
        :rtype:
        """
        print('Connect to mongo...')
        try:
            connect(host=db_uri, tlsCAFile=certifi.where())

            print('Successfully connected to mongo!')

        except ConnectionFailure as e:
            print(e)
            exit()

    # -- ON STARTUP --

    @staticmethod
    def init_coins() -> None:
        """
        Saves a list of active coins
        to the database if they are not there.

        :return:
        :rtype:
        """
        try:
            coin_list = Database.get_coins()

            if coin_list:
                return

            active_pairs = get_active_pairs()

            if active_pairs:
                CoinModel.objects.insert([CoinModel(symbol=symbol) for symbol in active_pairs], load_bulk=False)


        except Exception as e:
            print(e)

    @classmethod
    def on_startup(cls, db_uri: str) -> None:
        """
        Fires when the bot starts up to run
        the required database initialization methods

        :param db_uri: database connection string
        :type db_uri: str
        :return:
        :rtype:
        """
        cls.connect(db_uri=db_uri)
        cls.init_coins()

    # -- BINANCE --

    @staticmethod
    def get_coins() -> Optional[List[CoinModel]]:
        """
        Returns all pairs of coins that are in the database

        :return: List of all pairs of coins if any
        :rtype: Optional[List[database.models.coin_model.CoinModel]]
        """
        try:
            coins_list = CoinModel.objects()

            return coins_list

        except Exception as e:
            print(e)

    @staticmethod
    async def get_coin(symbol: str) -> Optional[CoinModel]:
        """

        :param symbol:
        :type symbol: str
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel]
        """
        try:
            coin: CoinModel = CoinModel.objects(symbol=symbol).first()

            return coin

        except Exception as e:
            print(e)

    @staticmethod
    async def write_last_data(symbol: str, last_price: float, last_timestamp: int) -> Optional[CoinModel]:
        """

        :param symbol:
        :type symbol: str
        :param last_price:
        :type last_price: float
        :param last_timestamp:
        :type last_timestamp: int
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel]
        """
        try:
            coin: CoinModel = CoinModel.objects(symbol=symbol).first()

            if coin:
                last_price = int(last_price * DELETE_ZEROS)
                last_timestamp = int(last_timestamp) + 10

                coin.last_timestamp = last_timestamp
                coin.last_price = last_price
                coin.save()

                return coin

        except Exception as e:
            print(e)

    @staticmethod
    async def treat_coin(symbol: str, price: int, timestamp: int, post_id: int) -> Optional[CoinModel]:
        """

        :param symbol:
        :type symbol: str
        :param price:
        :type price: int
        :param timestamp:
        :type timestamp: int
        :param post_id:
        :type post_id: int
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel]
        """
        print('--> Treat coin')
        try:
            coin: CoinModel = CoinModel.objects(symbol=symbol).first()

            if coin:
                new_post = PostModel(post_id=post_id).save()

                timestamp = timestamp + 10

                coin.status = 'treated'
                coin.open_target = randint(1, 4)
                coin.price = price
                coin.timestamp = timestamp
                coin.post = new_post
                coin.save()

                print('Treat coin --> ')

                return coin

        except Exception as e:
            print(e)

    @staticmethod
    async def change_post_status(post_id: int) -> Optional[bool]:
        """

        :param post_id:
        :type post_id: int
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel]
        """
        try:
            post: PostModel = PostModel.objects(post_id=post_id).first()

            if post:
                post.to_delete = False
                post.save()

                return True

        except Exception as e:
            print(e)

    @staticmethod
    async def delete_post(post_id: int) -> Optional[bool]:
        """

        :param post_id:
        :type post_id: int
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel
        """
        try:
            post: PostModel = PostModel.objects(post_id=post_id).first()

            if post:
                post.delete()

            return True

        except Exception as e:
            print(e)

    @staticmethod
    async def return_coin_to_pool(symbol: str) -> Optional[CoinModel]:
        """

        :param symbol: str
        :type symbol:
        :return:
        :rtype: Optional[database.models.coin_model.CoinModel]
        """
        try:
            coin: CoinModel = CoinModel.objects(symbol=symbol).first()

            if coin:
                coin.status = 'untreated'
                coin.price = None
                coin.timestamp = None
                coin.last_price = None
                coin.last_timestamp = None
                coin.entered_targets = None

                if coin.post:
                    coin.post.delete()

                coin.save()

                return coin

        except Exception as e:
            print(e)

    @staticmethod
    def add_target(symbol: str, target: float) -> Optional[CoinModel]:
        print(f'Add target {target}')
        try:
            coin: CoinModel = CoinModel.objects(symbol=symbol).first()

            if coin:
                coin.update(push__entered_targets=target)

                return coin

        except Exception as e:
            print(e)

    # -- STATISTIC --

    @staticmethod
    def write_daily_statistic(symbol: str, percent: float, period: str):
        """

        :param symbol:
        :type symbol: str
        :param percent:
        :type percent: float
        :param period:
        :type period: str
        :return:
        :rtype:
        """

        start_date = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            coin_statistic: DailyCoinStatisticModel = DailyCoinStatisticModel.objects(symbol=symbol,
                                                                                      date__gte=start_date,
                                                                                      date__lte=end_date).first()

            if coin_statistic:
                coin_statistic.delete()
            daily_statistic = DailyCoinStatisticModel(symbol=symbol, percent=percent, period=period,
                                                      date=datetime.now().strftime("%Y-%m-%d %H:%M")).save()

            return daily_statistic

        except Exception as e:
            print(e)

    @staticmethod
    async def get_daily_statistic() -> Optional[List[DailyCoinStatisticModel]]:
        """

        :return:
        :rtype:
        """
        start_date = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            statistic = DailyCoinStatisticModel.objects(date__gte=start_date, date__lte=end_date)

            if statistic:
                return statistic
        except Exception as e:
            print(e)

    @staticmethod
    async def get_monthly_statistic() -> Optional[Dict]:
        """

        :return:
        :rtype:
        """

        def get_suffix(day: int):
            """

            :param day:
            :type day: int
            :return:
            :rtype:
            """
            if 4 <= day <= 20 or 24 <= day <= 30:
                return "th"
            else:
                return ["st", "nd", "rd"][day % 10 - 1]

        date = (datetime.now() - timedelta(days=1))
        y_m = ('{dt.year} {dt.month}'.format(dt=date))
        year, month = map(int, y_m.split())
        num_days = monthrange(year, month)[1]
        month_name = date.strftime("%B")

        monthly_statistic = [year, month, month_name]
        try:
            for i in range(num_days):
                date_str = f"{i + 1}/{month}/{year}"
                date_time_obj = datetime.strptime(date_str, '%d/%m/%Y')

                s: List[DailyCoinStatisticModel] = DailyCoinStatisticModel.objects(
                    date__gte=date_time_obj, date__lte=date_time_obj + timedelta(hours=23, minutes=59, seconds=59))

                suffix = get_suffix(i + 1)
                if s:
                    daily_statistic = {
                        "day": f"{i + 1}{suffix} {month_name}",
                        "statistic": s
                    }

                    monthly_statistic.append(daily_statistic)

            return monthly_statistic

        except Exception as e:
            print(e)

    # -- INSTAGRAM --

    @staticmethod
    def get_last_ig_post() -> Optional[IGPostModel]:
        """

        :return:
        :rtype:
        """
        try:
            return IGPostModel.objects.order_by('-id').first()

        except Exception as e:
            print(e)

    @staticmethod
    def create_ig_post(symbol: str) -> Optional[bool]:
        """

        :param symbol:
        :type symbol:
        :return:
        :rtype:
        """
        try:
            IGPostModel(symbol=symbol, date=datetime.now()).save()

            return True

        except Exception as e:
            print(e)


def get_active_pairs() -> Optional[List[str]]:
    """
    Downloads all coins from binance,
    selects only pairs with bitcoin
    and selects active ones

    :return: Active coins, if any
    :rtype: Optional[List[str]]
    """

    client = Client()
    symbols = [symbol["symbol"] for symbol in client.get_exchange_info()["symbols"] if
               symbol["symbol"][-1:-4:-1] == "CTB"]  # получаем все пары монеты с BTC

    active_symbols = []
    for symbol in symbols:
        klines = client.get_klines(symbol=symbol, limit=2, interval="1m")
        if klines and time() - klines[0][6] / 1000 < 3600:
            active_symbols.append(symbol)

    return active_symbols

