from optibook.synchronous_client import Exchange
import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import sentimentanalysis
from threading import Thread, Lock
#from time import time, sleep
import time 


e=Exchange()
_ = e.connect()

if e.is_connected(): 
    print('Connected')

stocks = ['NVDA', 'CSCO', 'ING', 'PFE', 'SAN']
stocks_id = ['NVDA', 'CSCO', 'ING', 'PFE', 'SAN', 'Other']

stocks_ci={'NVDA':0,'CSCO':0,'ING':0,'PFE':0,'SAN':0}
stocks_time={'NVDA':0,'CSCO':0,'ING':0,'PFE':0,'SAN':0}
stocks_ask={'NVDA':0,'CSCO':0,'ING':0,'PFE':0,'SAN':0}
stocks_buy={'NVDA':0,'CSCO':0,'ING':0,'PFE':0,'SAN':0}


def clearOutstandingOrders(stock):
    if e.get_outstanding_orders(stock) > 0:
            e.delete_orders(stock)

# returns the best ask and the best bid
def getBestPrices(stock):
    book = e.get_last_price_book(stock) 
    return book.asks[0].price, book.bids[0].price

def getSpread(stock): 
    ask, bid = getBestPrices(stock)
    return ask - bid 
    
def getMidPrice(stock): 
    ask, bid = getBestPrices(stock)
    return (ask - bid) / 2

def getVolumeAdjustedMidPrice(stock): 
    book = e.get_last_price_book(stock) 
    volume_ask = book.asks[0].volume
    price_ask = book.asks[0].price
    volume_bid = book.bids[0].volume
    price_bid = book.bids[0].price
    weighted_mid = (volume_ask * price_ask + volume_bid * price_bid) / (volume_ask + volume_bid)
    return weighted_mid

def updateConfidence(): 
    news_data = e.poll_new_social_media_feeds()
    for news in news_data:
        name,sentiment =sentimentanalysis.analyseQuote(news.post)
        if name in stocks_ci:
            stocks_ci[name]=sentiment
            #print(stocks_ci[name])

def getConfidence(stock): 
    return stocks_ci[stock]

def neutraliseStock(stock): 
    ask, _ = getBestPrices(stock)
    out_orders=e.get_outstanding_orders(stock)
    for order in out_orders:
        if out_orders[order].price>ask and out_orders[order].side=='ask':
             e.amend_order(stock,order_id=order,volume=0)

# after a time limit, clear all orders for a given stock
def clearOrderTime(stock, time_limit): 
    if time()-stocks_time[stock]>time_limit:
        stocks_ci[stock]=0
        if len(e.get_outstanding_orders(stock))>0:
            e.delete_orders(stock)

def clearOrder(stock): 
    if len(e.get_outstanding_orders(stock))>0:
            e.delete_orders(stock)

def getPosition(stock):
    pos = e.get_positions()[stock]
    return pos 

def resetConfidence(stocks_ci):
    stocks_ci = {'NVDA':0,'CSCO':0,'ING':0,'PFE':0,'SAN':0}


def run(bullish_margin, bullish_vol, bearish_margin, bearish_vol): 

    for stock in stocks:

        spread = getSpread(stock)
        #mid_price = getMidPrice(stock)
        mid_price = getVolumeAdjustedMidPrice(stock)

        # neutraliseStock(stock)
        # clearOrders(stock, 3.0)

        # BULLISH
        if getConfidence(stock) > 0:
            if getPosition(stock) == 0: 
                e.insert_order(stock,price=mid_price-(bullish_margin*spread),volume=bullish_vol,side='bid',order_type='limit')
            else: 
                clearOrder(stock)
                e.insert_order(stock,price=mid_price-(bullish_margin*spread),volume=bullish_vol,side='bid',order_type='limit')
            time.sleep(2.5)
            resetConfidence(stocks_ci)
            e.insert_order(stock,price=mid_price+(bullish_margin*spread),volume=bullish_vol,side='ask',order_type='limit')

        # BEARISH 
        elif getConfidence(stock) < 0:

            if getPosition(stock) == 0: 
                e.insert_order(stock,price=mid_price-(bearish_margin*spread),volume=bearish_vol,side='ask',order_type='limit')
            else: 
                clearOrder(stock)
                e.insert_order(stock,price=mid_price-(bearish_margin*spread),volume=bearish_vol,side='ask',order_type='limit')
            time.sleep(2.5)
            resetConfidence(stocks_ci)
            e.insert_order(stock,price=mid_price-(bearish_margin*spread), volume=bearish_vol,side='bid',order_type='limit')

        time.sleep(0.1)


while True:
    # updates confidence from news s
    updateConfidence()
    # make buy and sells dependent on if we are bullish or bearish on a stock 
    run(bullish_margin=0.1, bullish_vol=99, bearish_margin=0.3, bearish_vol=99)

    