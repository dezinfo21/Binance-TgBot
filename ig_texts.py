ADMIN_USERNAME = "@channel_support_team"
ADMIN_LINK = "https://t.me/channel_support_team"


admin_name_texts = [
    f"Posted by {ADMIN_LINK}",
    f"Copyright by {ADMIN_LINK}",
    f"Signal by {ADMIN_LINK}"
]

binance_proof_texts = [
    lambda symbol, target, profit, period:
    f"This is a visual report of our pump. {symbol}BTC https://www.binance.com/en/trade/{symbol}_BTC?layout=pro\n"
    f"👈You can click on the link and see the process in real time on Binance🚀\n"    
    f"👍 {target} Target🎯 achieved in just: {period}\n"
    f"Profit: {profit}% for members who subscribed to our VIP channel.\n"
    f"\nOur price list for 👑VIP membership posted here 👉https://t.me/crypto_signals_binance_pump/44",
    lambda symbol, target, profit, period:
    f"✅Now we started pumping 👉 {symbol}BTC https://www.binance.com/en/trade/{symbol}_BTC?layout=pro\n"
    f"👍 {target} Target🎯 achieved in: {period}\n"
    f"Take profit: {profit}% for our VIP members\n"
    f"If you want to know about all our upcoming 🚀pumps, then you need to buy a subscription to the 👑VIP channel.",
    lambda symbol, target, profit, period:
    f"The our pump of coin 👉 {symbol}BTC https://www.binance.com/en/trade/{symbol}_BTC?layout=pro continues!\n"
    f"✅Now {target} Target🎯 has been achieved in: {period}\n"
    f"Quick profit: {profit}% for all members of our VIP channel.\n"
    f"Do you want to receive the same quick profit as all our 👑VIP members? Subscribe to our VIP channel.\n"
    f"Instructions for obtaining VIP access are written here 👉https://t.me/crypto_signals_binance_pump/44",
    lambda symbol, target, profit, period:
    f"This is a report about the our pump🚀 of the coin 👉 {symbol}BTC https://www.binance.com/en/trade/{symbol}_BTC?layout=pro\n"
    f"✅Now {target} Target🎯 has been achieved in: {period}\n"
    f"\nYou could also get {profit}% same value of profit if you bought a subscription to our 👑VIP channel in advance.\n"
    f"\n☎Contact: {ADMIN_LINK}"
]
tg_proof_texts = [
    "📌This signal was published on our 👑VIP channel before the start of our pump."
    "👆See proof of the accuracy of our information. This is a screenshot of the signal that we sent to our VIP channel in advance.\n"
    f"\nTo join the 👑VIP write to {ADMIN_LINK}",
    "🔔This is the proof of signal👆 that we gave earlier in the our 👑VIP channel",
    "🔥This is proof👆 that we wrote in our 👑VIP channel before we started pumping this coin.",
    "🔑Our VIP members received this signal👆 in the 👑VIP channel in advance, so they were able to take profit now💰!",
    "👆This is a proof of the signal that was published in our 👑VIP channel before the pump started."
]

statistic_texts = [
    "\n🔊If you want to get the same profit💰, then you need to purchase a subscription to our 👑VIP-channel.\n"
    "\nInstructions on how to access the 👑VIP channel are written here 👉https://t.me/crypto_signals_binance_pump/44\n"
    "\n⏰Today I will write the names of the next 10-15 coins in the our 👑VIP-Chanel.\n"
    "\nI tell you over and over again that these coins will give you an easy from 5% to 45% profit🤑🤑\n"
    "\n👉Our members make money easily with our signals and recover their VIP-fees costs with one-day signals🔔.\n"
    "\n📌Now the choice is yours: Get rich quickly or stay as you are now.🤔\n"
    f"\n☎Contact: {ADMIN_LINK} for buy VIP-membership!"
]
