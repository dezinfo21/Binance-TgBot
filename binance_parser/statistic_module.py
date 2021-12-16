from aiogram.types import ParseMode
from typing import List, Optional
from random import choice, randint

from binance_parser.social_media_module import IGPublisher
from database import Database
from loader import dp
from database.models import DailyCoinStatisticModel, MonthlyStatisticModel
import texts
import ig_texts
from data.config import PUBLIC_CHANNEL_ID


async def process_daily_statistic() -> None:
    """

    :return:
    :rtype:
    """
    try:
        statistic: List[DailyCoinStatisticModel] = await Database.get_daily_statistic()
        if statistic:
            post_body = ""
            total_percent = .0

            for stat in statistic:
                post_body += f"✅ {stat.symbol} {stat.percent}% within {stat.period}\n"
                total_percent += stat.percent

            total_percent = round(total_percent, 2)

            text_num = randint(0, len(texts.statistic_texts) - 1)

            text = f"🔥🔥 <b>Profit report for the last 24 hours</b> 🚀🚀\n" \
                   f"\n{post_body}\n" \
                   f"<b>Total profit {total_percent}%</b> 💰💰🤑\n" \
                   f"\n{texts.statistic_texts[text_num]}"

            post_link = (await dp.bot.send_message(chat_id=PUBLIC_CHANNEL_ID,
                                                   text=text,
                                                   parse_mode=ParseMode.HTML,
                                                   disable_web_page_preview=True)).url

            print("Statistic successfully posted!")

            if await process_daily_ig_statistic(post_link, statistic, total_percent, text_num):
                print('Successfully published daily statistic to Instagram and Facebook')

    except Exception as e:
        print(e)


async def process_monthly_statistic() -> None:
    """

    :return:
    :rtype:
    """
    try:
        statistic = await Database.get_monthly_statistic()
        if statistic:
            text = f"🔥🔥 <b>{statistic[2]} profit results</b> 💰💰👇\n\n"
            posts_id = []
            for daily_st in range(3, len(statistic)):
                daily_text = f"〰〰〰〰<b>{statistic[daily_st]['day']}</b>〰〰〰〰\n"
                for day in statistic[daily_st]['statistic']:
                    symbol = day.symbol
                    percent = day.percent
                    period = day.period

                    target_text = f"✅ {symbol} {percent}% within {period}\n"
                    daily_text += target_text

                if len(daily_text) + len(text) >= 3800:
                    text += f"\n☎ Contact <a href='{texts.ADMIN_LINK}'>{texts.ADMIN_USERNAME}</a>"

                    message = await dp.bot.send_message(chat_id=PUBLIC_CHANNEL_ID, text=text,
                                                        parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                    if message:
                        posts_id.append(message.message_id)

                    text = ""
                    text += daily_text

                    if daily_st == len(statistic) - 1:
                        text += f"\n☎ Contact <a href='{texts.ADMIN_LINK}'>{texts.ADMIN_USERNAME}</a>"

                        message = await dp.bot.send_message(chat_id=PUBLIC_CHANNEL_ID, text=text,
                                                            parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                        if message:
                            posts_id.append(message.message_id)
                elif daily_st == len(statistic) - 1:
                    text += daily_text
                    text += f"\n☎ Contact <a href='{texts.ADMIN_LINK}'>{texts.ADMIN_USERNAME}</a>"

                    message = await dp.bot.send_message(chat_id=PUBLIC_CHANNEL_ID, text=text,
                                                        parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                    if message:
                        posts_id.append(message.message_id)
                else:
                    text += daily_text

            MonthlyStatisticModel(year=statistic[0], month=statistic[1], posts_id=posts_id).save()

            print('Successfully published monthly statistic')

    except Exception as e:
        print(e)


async def process_daily_ig_statistic(post_link: str, statistic: List[DailyCoinStatisticModel], total_percent: float,
                                     text_num: int) -> Optional[bool]:
    """

    :param post_link:
    :type post_link:
    :param statistic:
    :type statistic:
    :param total_percent:
    :type total_percent:
    :param text_num:
    :type text_num:
    :return:
    :rtype:
    """
    post_body = ''
    text = ''

    try:
        if statistic:
            statistic_len = len(statistic)

            if statistic_len > 10:
                for stat in statistic[:5]:
                    post_body += f"✅ {stat.symbol[1:]} {stat.percent}% within {stat.period}\n"

                post_body += '\n(ｏ・_・)ノ ”(ᴗ_ ᴗ。)\n\n'

                for stat in statistic[statistic_len-5:]:
                    post_body += f"✅ {stat.symbol[1:]} {stat.percent}% within {stat.period}\n"

                text = f"🔥🔥 Profit report for the last 24 hours 🚀🚀\n" \
                       f"\n{post_body}\n" \
                       f"Total profit {total_percent}% 💰💰🤑\n\n" \
                       f"The full statistic you can find here 👉 {post_link}\n" \
                       f"\n{ig_texts.statistic_texts[text_num]}"

            else:
                for stat in statistic:
                    post_body += f"✅ {stat.symbol[1:]} {stat.percent}% within {stat.period}\n"

                    text = f"🔥🔥 Profit report for the last 24 hours 🚀🚀\n" \
                           f"\n{post_body}\n" \
                           f"Total profit {total_percent}% 💰💰🤑\n" \
                           f"More information you can find here 👉 {post_link}\n" \
                           f"\n{ig_texts.statistic_texts[text_num]}"

            return await IGPublisher.publish_post(text)

    except Exception as e:
        print(e)
