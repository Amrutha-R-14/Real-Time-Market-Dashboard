# Real-Time Market Data Streaming & Analytics Dashboard

## Description
This project is a real-time market data streaming and analytics dashboard built using Dash (Plotly), Python, and Pandas. It simulates or fetches live stock price data and visualizes both price trends and order book activity. The project demonstrates real-time data ingestion, visualization, and analytics, concepts commonly applied in financial trading platforms and big data pipelines.

## Project Structure
realtime_market/
 - dashboard.py 
 - market_simulator.py
 - analytics.py
 - order_book.py
 - requirements.txt 
 - README.md 

## Requirements
The required Python libraries are listed below:
- dash
- plotly
- pandas
Install with requirements.txt

## Output 
- Price over Time → Line graph showing live simulated stock price changes
- Order Book → Horizontal bar chart showing bid and ask volumes at different price levels

## Future Enhancements 
- Connect to real-time APIs (Yahoo Finance, Alpha Vantage)
- Add technical indicators like RSI, MACD, and Moving Averages
- Support for multiple stock tickers
- Database integration for storing historical market data
