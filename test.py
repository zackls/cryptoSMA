
import unittest
from binance_socket import BinanceSocket
import time
import logging
import threading

# these tests are pretty dependent on internet connection, so theyre put to sleep sometimes. if they flake on you, try increasing the sleep time
class TestBinanceSocket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.CRITICAL)

    def setUp(self):
        self.socket = None

    def testCallback(self):
        self.called = False
        def on_price(time, price):
            self.assertNotEqual(time, None)
            self.assertNotEqual(price, None)
            self.called = True

        self.socket = BinanceSocket(pair='tusdbtc', on_price=on_price)

        thread = threading.Thread(target=self.socket.start)
        thread.daemon = True
        thread.start()

        self.assertFalse(self.called)

        time.sleep(5)

        self.assertTrue(self.called)

        self.socket.close()

    def testClose(self):
        self.socket = BinanceSocket(pair='tusdbtc', on_price=lambda *args: None)

        thread = threading.Thread(target=self.socket.start)
        thread.daemon = True
        thread.start()
        time.sleep(1)

        self.assertTrue(self.socket.is_open)

        self.socket.close()
        time.sleep(1)

        self.assertFalse(self.socket.is_open)


if __name__ == '__main__':
    unittest.main()