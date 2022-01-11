from os import system
import pandas as pd
import math
import datetime
import time
from jugaad_trader import Zerodha
from optionchain_stream import OptionChain
kite = Zerodha()

def next_expiry():
    today = datetime.datetime.today()
    next_thursday = today + datetime.timedelta(((3 - today.weekday()) % 7))
    return datetime.datetime.strftime(next_thursday, '%Y-%m-%d')


def order(symbol,side):
    order_resp = kite.place_order(variety=kite.VARIETY_REGULAR,
			tradingsymbol=symbol,
			exchange=kite.EXCHANGE_NFO,
			transaction_type=  kite.TRANSACTION_TYPE_BUY if side == 'B' else kite.TRANSACTION_TYPE_SELL,
			quantity=25,
			order_type=kite.ORDER_TYPE_MARKET,
			product=kite.PRODUCT_MIS)
    print(order_resp)
    time.sleep(5)
 
def order_sl(symbol,side,trigger_price):
    # variety=regular&exchange=NFO&tradingsymbol=BANKNIFTY2211337800PE&transaction_type=BUY&order_type=SL&quantity=25
    # &price=253&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price=253&squareoff=0&stoploss=0&trailing_stoploss=0&user_id=ZD0120
    order_resp = kite.place_order(variety=kite.VARIETY_REGULAR,
			tradingsymbol=symbol,
			exchange=kite.EXCHANGE_NFO,
			transaction_type=kite.TRANSACTION_TYPE_BUY if side == 'B' else kite.TRANSACTION_TYPE_SELL,
			quantity=25,
			order_type=kite.ORDER_TYPE_SL,
			product=kite.PRODUCT_MIS,
            trigger_price=trigger_price)
    print(order_resp)
    time.sleep(5)

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


spot =  kite.quote('NSE:NIFTY BANK')
print(spot['NSE:NIFTY BANK']['last_price'])
spot = spot['NSE:NIFTY BANK']['last_price']
spot = math.floor(spot/100)*100  


pkl = pd.read_pickle('./banknifty.pkl')
pkl = pkl[pkl.expiry == next_expiry()]
pkl = pkl[pkl.strike.between(spot - 1000,spot + 1000)]
pkl_pe_sell = pkl[(pkl.instrument_type == 'PE') & (pkl.strike  == spot - 300)]
pkl_ce_sell = pkl[(pkl.instrument_type == 'CE') & (pkl.strike  == spot + 300)]
pkl_pe_buy = pkl[(pkl.instrument_type == 'PE') & (pkl.strike  == spot - 900)]
pkl_ce_buy = pkl[(pkl.instrument_type == 'CE') & (pkl.strike  == spot + 900)]


order(pkl_pe_buy.tradingsymbol,'B')
order(pkl_ce_buy.tradingsymbol,'B')
order(pkl_pe_sell.tradingsymbol,'S')
order(pkl_ce_sell.tradingsymbol,'S')

time.sleep(10)

orders = kite.orders()
print(orders)

# Get profile
# profile = kite.profile()
# print(profile)

# # Get margin
# margins = kite.margins()
# print(margins)

# # Get holdings
# holdings = kite.holdings()
# print(holdings)

# # Get today's positions
# positions = kite.positions()
# print(positions)

# # Get today's orders
# orders = kite.orders()
# print(orders)

# instrument_list=kite.instruments(exchange='NSE')
# print(instrument_list)

# Finally placing an order ZD
# order_resp = kite.place_order(variety=z.VARIETY_REGULAR,
# 			tradingsymbol="INFY",
# 			exchange=kite.EXCHANGE_NSE,
# 			transaction_type=kite.TRANSACTION_TYPE_BUY,
# 			quantity=1,
# 			order_type=kite.ORDER_TYPE_MARKET,
# 			product=kite.PRODUCT_CNC)
# print(order_resp)


# variety=regular&exchange=NFO&tradingsymbol=BANKNIFTY2211337800PE&transaction_type=BUY&order_type=SL&quantity=25
# &price=253&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price=253&squareoff=0&stoploss=0&trailing_stoploss=0&user_id=ZD0120