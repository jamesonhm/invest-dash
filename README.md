# Dual Momentum Investing Dashboard

## Usage:
To run the container, use this docker command as a template;

```
docker run \
  -it \
  -v <path/to/appdata>:/invest_dash \
  -p <host_port>:9090
  jamesonhm/invest_dash:latest
```

## How it Works:

Updater 
- runs week-daily on an apscheduler background task
- iterate over a slice of a list of stock symbols
- polls the yahoo finance api to get the close price for the current symbol
- Calculates Smoothed Rate of Change for each symbol and stores this with TS in the local sqlite DB

App
- Returns list of top n symbols by momentum score
- symbols' timeseries of score presented in chart

Frontend
- use HTMX
- symbol-score table
- click-open chart for timeseries view

