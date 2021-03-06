ADMIN_USERNAME = "@channel_support_team"
ADMIN_LINK = "https://t.me/channel_support_team"


admin_name_texts = [
    f"Posted by <a href='{ADMIN_LINK}'>{ADMIN_USERNAME}</a>",
    f"Copyright by <a href='{ADMIN_LINK}'>{ADMIN_USERNAME}</a>",
    f"Signal by <a href='{ADMIN_LINK}'>{ADMIN_USERNAME}</a>"
]

binance_proof_texts = [
    lambda symbol, target, profit, period:
    f"This is a visual report of our pump. ๐ #{symbol}/BTC (<a href='https://www.binance.com/en/trade/{symbol}_BTC?layout=pro'>Binance</a>) "
    f"๐You can click on the link and see the process in real time on Binance๐\n"    
    f"๐ <b>{target} Target</b>๐ฏ achieved in just: <b>{period}</b>\n"
    f"Profit: <b>{profit}%</b> for members who subscribed to our VIP channel.\n"
    f"\nOur price list for ๐VIP membership posted here ๐https://t.me/crypto_signals_binance_pump/44",
    lambda symbol, target, profit, period:
    f"โNow we started pumping ๐ #{symbol}/BTC (<a href='https://www.binance.com/en/trade/{symbol}_BTC?layout=pro'>Binance</a>).\n"
    f"๐ <b>{target} Target</b>๐ฏ achieved in: <b>{period}</b>\n"
    f"Take profit: <b>{profit}%</b> for our VIP members\n"
    f"If you want to know about all our upcoming ๐pumps, then you need to buy a subscription to the ๐VIP channel.",
    lambda symbol, target, profit, period:
    f"The our pump of coin ๐ #{symbol}/BTC (<a href='https://www.binance.com/en/trade/{symbol}_BTC?layout=pro'>Binance</a>) continues!\n"
    f"โNow <b>{target} Target</b>๐ฏ has been achieved in: <b>{period}</b>\n"
    f"Quick profit: <b>{profit}%</b> for all members of our VIP channel.\n"
    f"Do you want to receive the same quick profit as all our ๐VIP members? Subscribe to our VIP channel.\n"
    f"Instructions for obtaining VIP access are written here ๐https://t.me/crypto_signals_binance_pump/44",
    lambda symbol, target, profit, period:
    f"This is a report about the our pump๐ of the coin ๐ #{symbol}/BTC (<a href='https://www.binance.com/en/trade/{symbol}_BTC?layout=pro'>Binance</a>)\n"
    f"โNow <b>{target} Target</b>๐ฏ has been achieved in: <b>{period}</b>\n"
    f"\nYou could also get <b>{profit}%</b> same value of profit if you bought a subscription to our ๐VIP channel in advance.\n"
    f"\nโContact: <a href='{ADMIN_LINK}'>{ADMIN_USERNAME}</a>"
]
tg_proof_texts = [
    "๐This signal was published on our ๐VIP channel before the start of our pump."
    "๐See proof of the accuracy of our information. This is a screenshot of the signal that we sent to our VIP channel in advance.\n"
    f"\nTo join the ๐VIP write to <a href='{ADMIN_LINK}'>{ADMIN_USERNAME}</a>",
    "๐This is the proof of signal๐ that we gave earlier in the our ๐VIP channel",
    "๐ฅThis is proof๐ that we wrote in our ๐VIP channel before we started pumping this coin.",
    "๐Our VIP members received this signal๐ in the ๐VIP channel in advance, so they were able to take profit now๐ฐ!",
    "๐This is a proof of the signal that was published in our ๐VIP channel before the pump started."
]

statistic_texts = [
    "\n๐If you want to get the same profit๐ฐ, then you need to purchase a subscription to our ๐VIP-channel.\n"
    "\nInstructions on how to access the ๐VIP channel are written here ๐https://t.me/crypto_signals_binance_pump/44\n"
    "\nโฐToday I will write the names of the next 10-15 coins in the our ๐VIP-Chanel.\n"
    "\nI tell you over and over again that these coins will give you an easy from 5% to 45% profit๐ค๐ค\n"
    "\n๐Our members make money easily with our signals and recover their VIP-fees costs with one-day signals๐.\n"
    "\n๐Now the choice is yours: Get rich quickly or stay as you are now.๐ค\n"
    f"\nโContact: {ADMIN_USERNAME} for buy VIP-membership!"
]

