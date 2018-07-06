
import websocket  # pip install websocket-client
import logging
import ast


class BinanceSocket:
    def __init__(self, pair, on_price, *args, **kwargs):
        ''' initializes a binance websocket with the provided info
             - pair: the pair to use for the socket
             - on_price: a method (time, price) which is called when
               the price is updated by the socket, and the time at
               which it was updated
        '''

        # provide some info
        logging.info('Initializing connection for {}. Input ctrl+c to exit.'.format(pair))
        logging.warning('Python loggers get hung up sometimes. If you\'re not seeing any output, try hitting a key to wake it up!')

        # initialize instance variables for use within methods
        self.on_price = on_price
        # open websocket connection, passing any additional args along
        self.ws = websocket.WebSocketApp(
            "wss://stream.binance.com:9443/ws/{}@ticker".format(pair),
            *args,
            on_message=self.on_message,
            on_close=self.on_close,
            **kwargs
        )
        self.is_open = False

    def start(self):
        self.is_open = True
        # run the websocket indefinitely
        self.ws.run_forever()


    def on_message(self, ws, message):
        ''' called when the socket receives data
             - ws: the socket itself
             - message: a string of the actual data
        '''

        # parse message
        parsed = ast.literal_eval(message)

        # check if the weighted average (w) and time (E) are in the message
        if 'w' in parsed and 'E' in parsed:
            call_time = int(parsed.get('E'))
            price = float(parsed.get('w'))

            # call the callback given to this class
            self.on_price(call_time, price)
        else:
            # the data 
            logging.error('Error with websocket message format - unknown price. Response: {}'.format(message))

    def on_close(self, ws):
        ''' let the user know the connection has successfully closed
        '''
        self.is_open = False
        logging.info('Connection closed successfully')

    def close(self):
        ''' simply close the connection
        '''
        self.ws.close()