
import logging
import argparse
from binance_socket import BinanceSocket


if __name__ == '__main__':
    # read the pair from the args, defaulting to tusdbtc
    parser = argparse.ArgumentParser(description='Opens a websocket to binance and outputs the 1-minute simple moving average of a certain currency pair every second.')
    parser.add_argument('-p', default='tusdbtc', type=str, help='the pair to use for the sma from binance, all lowercase and without spaces')
    args = parser.parse_args()

    pair = args.p

    # set logging level
    logging.basicConfig(level=logging.DEBUG)

    ws = None

    # if a keyboard interrupt occurs, we want to close the connection - better to be safe
    try:

        # 60-item array from the current second to the corresponding price
        # NOTE this could be a mapping from the mod of the second to the price, however the binance socket
        # is pretty inconsistent with timing, so to be safe, this is simply a rotating array
        minute_data = []

        # callback for when a price is read by the socket, happens every second
        def on_price(time, price):
            # convert time from ms to seconds
            time /= 1000
            # fill appropriate second in the price array
            minute_data.append(price)
            # if the data is longer than 60 points, remove the earliest item
            if len(minute_data) > 60:
                minute_data.pop(0)

            # calculate the sma
            sma = sum(minute_data) / len(minute_data)

            # print that bad boy out
            logging.info('Timestamp: {}, 1-Minute SMA: {}'.format(time, sma))

        # initialize socket with pair and callback
        ws = BinanceSocket(pair=pair, on_price=on_price)

    # ensure the connection is closed when exiting
    except KeyboardInterrupt as e:
        if ws:
            ws.close()
        raise e
