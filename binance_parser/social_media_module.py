import asyncio
from datetime import datetime
from random import choice, randint

import requests
from aiogram.types import ParseMode, InputFile

import ig_texts
import texts
from binance_config import BUY_ZONE_PERCENT_PLUS, BUY_ZONE_PERCENT_MINUS, SELL_ZONE_PERCENTS, DELETE_ZEROS
from data.config import TEMP_CHANNEL_ID, CHANNEL_ID, PUBLIC_CHANNEL_ID, API_BASE_URL, VIEWS_UP_CHANNEL_ID
from database import Database
from loader import dp
from . import ScreenshotModule


class TGPublisher:
    @staticmethod
    async def create_pump_post(symbol: str, price: float, timestamp: int) -> None:
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
        print(f'--> Create pump post for coin {symbol}')
        price = int(price * DELETE_ZEROS)

        post_title = f"#{symbol[:-3]}/BTC (<a href='https://www.binance.com/en/trade/{symbol[:-3]}_BTC?layout=pro'>Binance</a>)"

        buy_zone_plus = str(int(price + price * BUY_ZONE_PERCENT_PLUS / 100))
        buy_zone_minus = str(int(price - price * BUY_ZONE_PERCENT_MINUS / 100))
        post_buy_zone = f"<b>Buy zone</b>: {buy_zone_minus}-{buy_zone_plus}"

        post_sell_zone = "".join(
            f"🎯 <b>Target {i}</b>: {int(price + price * percent / 100)}\n"
            for i, percent in enumerate(SELL_ZONE_PERCENTS, 1)
        )

        post_timezone = "The signal publication time corresponds to the time zone:\n" \
                        "<a href='https://time.is/'>GMT +1</a>"

        post_sign = choice(texts.admin_name_texts) if randint(0, 100) <= 30 else ""

        text = f"{post_title}\n\n" \
               f"{post_buy_zone}\n\n" \
               f"{post_sell_zone}" \
               f"{post_timezone}\n" \
               f"{post_sign}"

        try:
            print('--> Send message to private channel')
            post_id = (await dp.bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode=ParseMode.HTML,
                                                 disable_web_page_preview=True)).message_id
            print('Send message to private channel --> ')
            if await Database.treat_coin(symbol=symbol, price=price, timestamp=timestamp, post_id=post_id):

                print('--> Send message to views up channel')
                # await dp.bot.send_message(chat_id=VIEWS_UP_CHANNEL_ID, text=text, parse_mode=ParseMode.HTML,
                #                           disable_web_page_preview=True)
                print('Send message to views up channel --> ')

                print('--> Send message to temp channel')
                temp_post_id = (await dp.bot.send_message(chat_id=TEMP_CHANNEL_ID, text=text,
                                                          parse_mode=ParseMode.HTML,
                                                          disable_web_page_preview=True)).message_id
                print('Send message to temp channel --> ')

                ScreenshotModule.make_tg_screen(symbol=symbol, post_sign=post_sign)

                await dp.bot.delete_message(chat_id=TEMP_CHANNEL_ID, message_id=temp_post_id)

                print(f'Create pump post for coin {symbol} -->')

        except Exception as e:
            print(e)

    @staticmethod
    async def create_target_enter_post(symbol: str, target_index: int, open_target: int, seconds: int, period: str,
                                       percent: float, post_id: int) -> None:
        """

        :param symbol:
        :type symbol: str
        :param target_index:
        :type target_index: int
        :param open_target:
        :type open_target: int
        :param seconds:
        :type seconds: int
        :param period:
        :type period: str
        :param percent:
        :type percent: float
        :param post_id:
        :type post_id: int
        :return:
        :rtype:
        """
        print(f'--> Create target enter post in IG for coin {symbol}')
        binance_img_path = ScreenshotModule.make_binance_screen(symbol)
        tg_img_path = ScreenshotModule.process_tg_screen(symbol=symbol, seconds=seconds, target_index=target_index,
                                                         open_target=open_target)

        binance_text_num = randint(0, len(texts.binance_proof_texts) - 1)
        binance_text = texts.binance_proof_texts[binance_text_num](symbol=symbol, target=target_index, profit=percent,
                                                                   period=period)

        binance_photo = InputFile(path_or_bytesio=binance_img_path)

        await dp.bot.send_photo(chat_id=PUBLIC_CHANNEL_ID,
                                photo=binance_photo,
                                caption=binance_text,
                                parse_mode=ParseMode.HTML)

        tg_text_num = randint(0, len(texts.tg_proof_texts) - 1)
        tg_text = texts.tg_proof_texts[tg_text_num]

        tg_photo = InputFile(path_or_bytesio=tg_img_path)

        await dp.bot.send_photo(chat_id=PUBLIC_CHANNEL_ID,
                                photo=tg_photo,
                                caption=tg_text,
                                parse_mode=ParseMode.HTML)

        text = f'<a href="https://www.binance.com/en/trade/{symbol}_BTC?layout=pro">Binance</a>\n' \
               f'#{symbol}/BTC Take-Profit target {target_index} ✅\n' \
               f'Profit: {percent}% 📈\n' \
               f'Period: {period} ⏰'

        try:
            await dp.bot.send_message(chat_id=CHANNEL_ID, text=text, reply_to_message_id=post_id,
                                      disable_web_page_preview=True)



        except Exception as e:
            print(e)

        await IGPublisher.create_target_enter_post(symbol=symbol, target_index=target_index, percent=percent,
                                                   period=period, binance_text_num=binance_text_num,
                                                   tg_text_num=tg_text_num, binance_image_path=binance_img_path,
                                                   tg_image_path=tg_img_path)

        print(f'Create target enter post in IG for coin {symbol} -->')

    @staticmethod
    async def delete_post(post_id: int) -> None:
        if await Database.delete_post(post_id):
            try:
                await dp.bot.delete_message(chat_id=CHANNEL_ID, message_id=post_id)
                print(f'Post with id {post_id} successfully deleted')

            except Exception as e:
                print(e)


class IGPublisher:
    """

    """

    @staticmethod
    async def create_target_enter_post(symbol: str, target_index: int, percent: float, period: str,
                                       binance_text_num: int, tg_text_num: int, binance_image_path: str,
                                       tg_image_path: str):
        """

        :param symbol:
        :type symbol:
        :param target_index:
        :type target_index:
        :param percent:
        :type percent:
        :param period:
        :type period:
        :param binance_text_num:
        :type binance_text_num:
        :param tg_text_num:
        :type tg_text_num:
        :param binance_image_path:
        :type binance_image_path:
        :param tg_image_path:
        :type tg_image_path:
        :return:
        :rtype:
        """
        print('--> Create instagram post')
        print(IGPublisher.can_create_post())
        if IGPublisher.can_create_post():
            try:
                # await asyncio.sleep(10)

                if IGPublisher.upload_photo(image_path=binance_image_path) \
                        and IGPublisher.upload_photo(image_path=tg_image_path):

                    print('image path', binance_image_path, tg_image_path)

                    binance_image = binance_image_path.split('\\')[-1]
                    tg_image = tg_image_path.split('\\')[-1]

                    print('images', binance_image, tg_image)

                    binance_text = ig_texts.binance_proof_texts[binance_text_num](symbol=symbol, target=target_index,
                                                                                  profit=percent, period=period)
                    tg_text = ig_texts.tg_proof_texts[tg_text_num]

                    if IGPublisher.publish_post(image=binance_image, post_text=binance_text):
                        print('Successfully published post from binance to Instagram')

                    # await asyncio.sleep(10)

                    if IGPublisher.publish_post(image=tg_image, post_text=tg_text):
                        print('Successfully published post from telegram to Instagram')

                    if Database.create_ig_post(symbol=symbol):
                        print('New Instagram post successfully saved to database')

                    print('Create instagram post -->')

            except Exception as e:
                print(e)

    @staticmethod
    def upload_photo(image_path: str):
        """

        :param image_path:
        :type image_path:
        :return:
        :rtype:
        """
        print('--> Upload Instagram photo')
        try:
            files = {
                'image': open(image_path, 'rb')
            }

            response = requests.post(url=f"{API_BASE_URL}images/upload", files=files)
            print(f'Response {response.text}')
            if response.status_code == 201:
                print('Upload Instagram photo -->')
                return True


        except Exception as e:
            print(e)

    @staticmethod
    def publish_post(post_text: str, image: str = None):
        """

        :param image:
        :type image:
        :param post_text:
        :type post_text:
        :return:
        :rtype:
        """
        print('--> Publish Instagram post')
        if not image:
            image = 'statistic_image.jpg'

        try:
            params = {
                "text": post_text,
                "img": image
            }

            response = requests.post(url=f"{API_BASE_URL}posts/create", params=params)
            print(f'Response {response.text}')
            if response.status_code == 200:
                print('Publish Instagram post -->')
                return True

        except Exception as e:
            print(e)

    @staticmethod
    def can_create_post():
        """

        :return:
        :rtype:
        """
        ig_post = Database.get_last_ig_post()

        if ig_post:
            date_now = datetime.now()

            return (date_now - ig_post.date).seconds >= 7200

        return True
