import time
from jugaad_trader import Zerodha
kite = Zerodha()
 
def order_square_off(symbol,side):
    # variety=regular&exchange=NFO&tradingsymbol=BANKNIFTY2211337800PE&transaction_type=BUY&order_type=SL&quantity=25
    # &price=253&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price=253&squareoff=0&stoploss=0&trailing_stoploss=0&user_id=ZD0120
    order_resp = kite.place_order(variety=kite.VARIETY_REGULAR,
			tradingsymbol=symbol,
			exchange=kite.EXCHANGE_NFO,
			transaction_type=kite.TRANSACTION_TYPE_BUY if side == 'B' else kite.TRANSACTION_TYPE_SELL,
			quantity=25,
			order_type=kite.ORDER_TYPE_MARKET,
			product=kite.PRODUCT_MIS,
            )
    print(order_resp)
    time.sleep(5)

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


orders = kite.orders()
trigger_pending_orders = list(filter(lambda order: order['status'] == 'TRIGGER PENDING',orders))
for order in trigger_pending_orders:
    print(kite.cancel_order(variety=kite.VARIETY_REGULAR,order_id=order['order_id']))


position = kite.positions()

open_position = list(filter(lambda pos: pos['quantity'] != 0,position['day']))
sell_open_position = list(filter(lambda pos: pos['quantity'] < 0,open_position))
buy_open_position = list(filter(lambda pos: pos['quantity'] > 0,open_position))

# print(open_position)

for pos in sell_open_position:
    print(pos['tradingsymbol'])
    order_square_off(pos['tradingsymbol'], 'B')

for pos in buy_open_position:
    print(pos['tradingsymbol'])
    order_square_off(pos['tradingsymbol'], 'S')