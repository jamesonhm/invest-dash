##Dual Momentum Investing strategy dashboard

#Outline

Updater 
- runs weekdaily on an apscheduler background task
- iterate over a slice of a list of stock symbols
- polls the yahoo finance api to get the close price for the current symbol
- Calculates Smoothed Rate of Change for each symbol and stores this with TS in the DB

APP
- Returns top n list of symbols by momentum score
- symbol timeseries of score presented in chart

Frontend
- use HTMX
- symbol-score table
- click-open chart for timeseries view

