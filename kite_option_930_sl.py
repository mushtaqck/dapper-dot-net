import time
from jugaad_trader import Zerodha
kite = Zerodha()
 
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
            trigger_price=trigger_price,
            price=trigger_price)
    print(order_resp)
    time.sleep(5)

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


orders = kite.orders()
completed_sell_orders = filter(lambda order: order['transaction_type'] == 'SELL' and order['status'] == 'COMPLETE',orders)
for order in completed_sell_orders:
    sl_order = list(filter(lambda order: order['tradingsymbol'] == order['tradingsymbol'] and order['status'] == 'TRIGGER PENDING',orders))
    if len(sl_order) == 0:
        order_sl(order['tradingsymbol'],'B', round(order['average_price'] + (order['average_price']/2))) 