import websocket  # pip install websocket-client
import socket  # pip install websocket-client
import time
import sys

if __name__ == '__main__':
    ws = None
    try:

        # 60-item mapping from the current second to the corresponding price
        btc_data = [None for x in xrange(60)]

        def on_message(ws, message):
            print message
            sys.stdout.flush()

        def on_close(ws):
            print 'Connection closed successfully'

        websocket.enableTrace(True)
        # using tether as a substitute for USD, since usd/btc doesnt exist on binance
        ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/tusdbtc@ticker",
            on_message=on_message,
            on_close=on_close,
        )
        ws.run_forever()

    except KeyboardInterrupt as e:
        if ws:
            ws.close()
        raise e
