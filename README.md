# Quant-Trading-Algorithm
### Table of Contents

1. [Project Motivation](#motivation)
2. [File Descriptions](#files)
3. [Results](#results)
4. [Licensing, Authors, and Acknowledgements](#licensing)

## Project Motivation<a name="motivation"></a>
A quantitative trading algorithm that makes trades based on semantic analysis of social media messages (and many other factors). The algorithm was developed for Hack The Burgh 2024. Our strategy was to bank on our semantic analysis rather than our market making by quickly and efficiently sending high volume asks/bids to captilise on price changes.

## File Descriptions <a name="files"></a>
Re-Connect.py -> Continually checks if a reconnect to the Optiver Trading API is required.
SemanticAnalysis.py -> Takes a social media message and outputs the prediction for 'Bearish' and 'Bullish', and the associated stock(s).
Trade.py -> Sends asks and bids into the market using factors including market spread, mid-point, the semantic analysis results, price history...
Neutralise.py -> Neutralises our position by sending asks/bids at the current mid point for the long/short stock.

## Results<a name="results"></a>
We peaked at 3rd out of 17 teams

## Licensing, Authors, Acknowledgements<a name="licensing"></a>
Matthew Davies
Michael Zhang
Hashim Al-Obaidi

