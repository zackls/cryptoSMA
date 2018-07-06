# Binance SMA Scraper

This project simply opens a websocket to Binance (docs [here](https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md)) and keeps a rolling 1-minute average of the provided currency pair, printing out that average every second.

Running `main.py` will kick off the websocket, with a single optional parameter `-p`, the currency pair to use. This defaults to `usdtbtc`.

## Dependencies

This project can be run using either `python2` or `python3`, and depends on `websocket-client` which can be installed with `pip install websocket-client`.

## Testing

There are some tests provided, in the `test.py` file.