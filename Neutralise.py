from optibook.synchronous_client import Exchange
from time import sleep

e = Exchange()

e.connect()

# neutralisation
pos=e.get_positions()
print(pos)
const=0.1
count=10
while count!=0:

    pos=e.get_positions()
    count=0
    for x in pos.values():
        count+=x
    print(count)
    for company in pos.keys():
        e.delete_orders(company)
        price_book=e.get_last_price_book(company)
        best_ask=price_book.asks[0].price
        best_bid=price_book.bids[0].price
        mid_price = (price_book.bids[0].price + price_book.asks[0].price) / 2
        spread=best_ask-best_bid
        if pos[company]>0:
            e.insert_order(company,price=best_ask-const*spread,volume=pos[company],side='ask',order_type='ioc')
        elif pos[company]<0:
            e.insert_order(company,price=best_bid+const*spread,volume=abs(pos[company]),side='bid',order_type='ioc')
        sleep(0.075)
    if const <1:
        const+=0.1