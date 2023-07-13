Outline

Crawler 
- runs week-daily on a cron job
- iterate over a list of symbols
- using one of several website obj's, pulls the close price and volume for the current symbol
- stores this with TS in the DB

API
- top n list of symbols by dual momentum score
  - dual momentum score calc'd in DB view?
- symbol timeseries of score and close price?

Frontend
- use HTMX?
- symbol-score tiles
- click-open chart? for timeseries view

