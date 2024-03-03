# -*- coding: utf-8 -*-

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pandas as pd
import numpy as np

model = AutoModelForSequenceClassification.from_pretrained('./')
tokenizer = AutoTokenizer.from_pretrained('./')
c = pipeline('zero-shot-classification', model=model, tokenizer=tokenizer)


df = pd.read_csv('/home/ubuntu/sentiment_analysis/training.csv')

stock_names = [i for i in df.columns[1:]]
sentiments = ['bearish', 'bullish']
categories = stock_names + ['Other']
category_dict = {'NVDA':0,
                 'ING':1,
                 'SAN':2,
                 'PFE':3,
                 'CSCO':4,
                 'Other':5}

def categoriseQuote(quote):
    stock_keywords = {
        'NVDA': ['Nvidia', 'NVIDIA', 'NVDA', 'nvidia'],
        'ING': ['ING'],
        'CSCO': ['Cisco', 'CISCO', 'CSCO', 'cisco', 'csco'],
        'PFE': ['Pfizer', 'PFIZER', 'PFE', 'pfizer', 'pfe'],
        'SAN': ['Santander', 'SANTANDER', 'SAN', 'santander',]
    }

    for stock, keywords in stock_keywords.items():
        # Check if any keyword is present as a substring in the quote
        if any(keyword in quote for keyword in keywords):
            return stock

    return 'Other'

def getSentiment(quote):
    output = c(quote, sentiments)

    # Extracting bullish, bearish, and neutral scores
    bullish = output['scores'][output['labels'].index('bullish')]
    bearish = output['scores'][output['labels'].index('bearish')]
    # neutral = output['scores'][output['labels'].index('neutral')]

    # Determine the max sentiment
    max_score = max(bullish, bearish)
    if max_score == bullish:
        return 1
    elif max_score == bearish:
        return -1
    
    
def analyseQuote(quote):
    return categoriseQuote(quote), getSentiment(quote)


