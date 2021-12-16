import decimal
import os
from typing import Optional

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

from defenitions import BINANCE_IMAGES_FOLDER_ROOT, TELEGRAM_IMAGES_FOLDER_ROOT

COLOR_WHITE = [255, 255, 255]


class ScreenshotModule:
    @staticmethod
    def make_binance_screen(symbol) -> Optional[str]:
        """

        :param symbol:
        :type symbol: str
        :return:
        :rtype:
        """
        print('make_binance_screen for ' + symbol)
        response = requests.get(
            url="https://api.screenshotmachine.com?"
                "key=f8f8eb"
                f"&url=https://www.binance.com/en/trade/{symbol}_BTC?layout=pro"
                "&device=desktop"
                "&dimension=1980x1020"
                "&format=png"
                "&cacheLimit=0"
                "&delay=5000"
                "&click=%23%5C31%205m"
                "&hide=body%20%3E%20div.css-1u2nk9f",
            timeout=30
        )

        if response:
            try:
                img_path = os.path.join(BINANCE_IMAGES_FOLDER_ROOT, f'binance_{symbol}BTC_screen.png')

                with open(img_path, "wb") as file:
                    file.write(response.content)

                img: Image = Image.open(img_path)

                crop_img: Image = img.crop((0, 60, 1320, 735))
                width, height = crop_img.size

                resized_img = crop_img.resize((1250, height))
                resized_img.save(img_path)
            except Exception as e:
                print(e)
            else:
                return img_path

    @staticmethod
    def make_tg_screen(symbol: str, post_sign: str) -> Optional[str]:
        response = requests.get(
            url="https://api.screenshotmachine.com?"
                "key=f8f8eb"
                "&url=https://t.me/s/test_binance_channel_kirill" 
                "&device=desktop"
                "&dimension=1980x1020"
                "&format=png"
                "&cacheLimit=0"
                "&delay=1000"
                "&click=%23%5C31%205m"
                "&hide=body%20%3E%20div.css-1u2nk9f",
            timeout=30
        )

        if response:
            try:
                img_path = os.path.join(TELEGRAM_IMAGES_FOLDER_ROOT, f'tg_{symbol}_screen.png')
                print("-->Call make_tg_screen")
                print('img_path  for tg image = '+ img_path)
                with open(img_path, "wb") as file:
                    file.write(response.content)

                img = Image.open(img_path).convert("RGB")
                if post_sign:
                    cut_img = img.crop((616, 655, 1600, 990))
                else:
                    cut_img = img.crop((616, 675, 1600, 990))

                img_arr = np.array(cut_img)
                Y, X = np.where(np.all(img_arr == COLOR_WHITE, axis=2))

                cut_img.save(img_path, quality=100, subsampling=0)
                crop_img = cut_img.crop((0, 0, max(X) + 5, max(Y) + 5))

                draw = ImageDraw.Draw(crop_img)

                draw.rectangle([(max(X) - 82, max(X) - 19), (max(X) - 40, max(X) - 2)], fill="#ffffff")

                crop_img.save(img_path, quality=100, subsampling=0)

                return img_path

            except Exception as e:
                print(e)

    @staticmethod
    def process_tg_screen(symbol: str, seconds: int, target_index: int, open_target: int) -> Optional[str]:
        """

        :param symbol:
        :type symbol: str
        :param seconds:
        :type seconds: int
        :param target_index:
        :type target_index: int
        :param open_target:
        :type open_target: int
        :return:
        :rtype:
        """
        try:
            img_path = os.path.join(TELEGRAM_IMAGES_FOLDER_ROOT, f'tg_{symbol}BTC_screen.png')
            print("-->Call process_tg_screen")
            print('img_path  for tg image = ' + img_path)
            img = Image.open(img_path).convert("RGB")
            views_icon = Image.open('tg_views_icon.png')
            vip_only_icon = Image.open('vip_only_icon.png')

            img_arr = np.array(img)
            Y, X = np.where(np.all(img_arr == COLOR_WHITE, axis=2))

            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("roboto_regular.ttf", 13)

            minutes = max(37, int(seconds / 60))
            if minutes < 1440:
                post_views = int(minutes * .8)
            elif 1440 < minutes < 7200:
                post_views = int(1440 * .8 + (minutes - 1440) * .5)
            elif 7200 < minutes < 14400:
                post_views = int(1440 * .8 + 5760 * .5 + (minutes - 7200) * .3)
            elif 14400 < minutes < 28800:
                post_views = int(1440 * .8 + 5760 * .5 + 7200 * .3 + (minutes - 14400) * .1)
            else:
                post_views = int(1440 * .8 + 5760 * .5 + 7200 * .3 + 14400 * .1 + (minutes - 28800) * 0.001)

            post_views = min(post_views, 4100)

            if post_views > 999:
                post_views = decimal.Decimal(str(round(post_views / 1000, 1))).normalize()
                post_views = '{0:.16f}'.format(post_views).strip('0') + "K"
                if post_views[-2] == ".":
                    post_views = post_views.replace(".", "")
                post_views = f"{post_views}"

            post_view_len = len(str(post_views))

            for i in range(target_index, 5):
                if i == open_target:
                    continue
                img.paste(vip_only_icon, (94, 154 + 20 * i))

            draw.rectangle([(max(X) - 102, max(Y) - 19), (max(X) - 40, max(Y) - 2)], fill="#ffffff")

            draw.text(xy=(max(X) - 47 - 7 * post_view_len, max(Y) - 19), text=f"{post_views}", align="right",
                      fill="#738ca7",
                      font=font)

            img.paste(views_icon, (max(X) - 67 - 7 * post_view_len, max(Y) - 16))

            final_img_path = os.path.join(TELEGRAM_IMAGES_FOLDER_ROOT, f'tg_final_{symbol}BTC_screen.png')

            img.save(final_img_path)

            return final_img_path

        except Exception as e:
            print(e)
