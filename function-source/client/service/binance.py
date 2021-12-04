import ccxt
from retry import retry
from ccxt.base.errors import ExchangeNotAvailable
from client.service.exchange import ExchangeService
import time

# -------------------------------
# BinanceService Class
# -------------------------------
class BinanceService(ExchangeService):
    
    def __init__(self, symbol, config, exchange, on_error):
        super().__init__(config, exchange, on_error)
        self.binance = ccxt.binance({
            'apiKey': config.get('settings', 'API_KEY'), 
            'secret': config.get('settings', 'API_SECRET'), 
            'options': {'defaultType': 'future'},
            'enableRateLimit': True,
            'timeout': 100000,
        }) 
        self.binance.set_sandbox_mode(config.getboolean('settings', 'TESTNET')) # debugmode
        self.binance.verbose = config.getboolean('settings', 'DEBUG')
        self.binance.load_markets()
        #self.symbol = self.find_symbol(self.binance, symbol)
        self.symbol = symbol
        self.binance.fapiPrivate_post_leverage({
            'symbol' : self.symbol,
            'leverage' : self.flexible_leverage,    
        })
        # potiosion mode
        positionmode = self.binance.fapiPrivate_get_positionside_dual()
        if not positionmode['dualSidePosition']:
            positionmode = self.binance.fapiPrivate_post_positionside_dual({
                'dualSidePosition' : True, 
            })
        else:
            pass
        self.balance = round(float(self.__get_balance()), 2)

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __get_balance(self):
        balance = self.binance.fetch_balance()
        return balance['USDT']['total']

    #@retry(ExchangeNotAvailable, tries=100, delay=0.25)
    #def __get_best_price(self):
    #    ticker = self.binance.fetch_ticker(self.symbol)
    #    ticker = self.binance.fetch_tickers()[self.symbol]
    #    return (float)(ticker['info']['bid_price']), (float)(ticker['info']['ask_price'])

    @retry(ExchangeNotAvailable, tries=100, delay=0.25) 
    def __create_entry_order(self, buy):
        self.side = 'BUY' if buy else 'SELL'
        tpsl_side = 'SELL' if buy else 'BUY'
        positionside = 'LONG' if buy else 'SHORT'
        if self.fixed_lot:
            self.entry_amount = self.fixed_lot_size
        else:
            self.entry_amount = round(self.balance / 1000 * self.flexible_lot_percent, 3)
            if self.entry_amount < 0.001:
                self.entry_amount = 0.001
        self.binance.fapiPrivate_post_order({
            'symbol' : self.symbol,
            'side' : self.side,
            'positionSide' : positionside,
            'type' : 'MARKET',
            'quantity' : self.entry_amount,
        })
        # takeprofit
        self.binance.fapiPrivate_post_order({
            'symbol' : self.symbol,
            'side' : tpsl_side,
            'positionSide' : positionside,
            'type' : 'TAKE_PROFIT_MARKET',
            'quantity' : self.entry_amount,
            'stopPrice' : self.entry_tp,
        })
        # stoploss
        self.binance.fapiPrivate_post_order({
            'symbol' : self.symbol,
            'side' : tpsl_side,
            'positionSide' : positionside,
            'type' : 'STOP_MARKET',
            'quantity' : self.entry_amount,
            'stopPrice' : self.entry_sl,
        })
        #self.binance.create_order(self.symbol, 'market', self.side, self.entry_amount, params=params)
        return

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __create_exit_order(self, buy):
        self.side = 'SELL' if buy else 'BUY'
        positionside = 'LONG' if buy else 'SHORT'
        self.binance.fapiPrivate_post_order({
            'symbol' : self.symbol,
            'side' : self.side,
            'positionSide' : positionside,
            'type' : 'MARKET',
            'quantity' : self.exit_amount,
        })
        # cancel all orders
        self.binance.cancel_all_orders(self.symbol)        
        #self.binance.create_order(self.symbol, 'market', self.side, self.exit_amount, params=params)
        return

    def fetch_positions(self):
        orders = self.binance.fetch_account_positions()
        order = [x['info']['positionAmt'] for x in orders if x['info']['symbol'] == self.symbol]
        print('\norder: {}'.format(order))
        if len(order) <= 1:
            self.exit_amount = 0.0
            return False
        elif order[1] != '0.000' or order[2] != '0.000' :
            self.exit_amount = abs(float(order[1])) if order[1] != '0.000' else abs(float(order[2]))
            print('\nexit_amount: {}'.format(self.exit_amount))
            return True
        else:
            self.exit_amount = 0.0
            return False

    def entry_order(self, buy):
        try:
            self.__create_entry_order(buy)
            self.balance = round(float(self.__get_balance()), 2)
        except:
            self.on_error('entry_order::create_order')

    def exit_order(self, buy):
        try:
            self.__create_exit_order(buy)
            self.balance = round(float(self.__get_balance()), 2)
            endtime = round(time.time() * 1000)
            starttime = round(endtime - 3896000)
            trades = self.binance.fetch_my_trades(self.symbol, starttime)
            trades = [x['info']['realizedPnl'] for x in trades if x['info']['symbol'] == self.symbol]
            self.closed_pnl = round(float(trades[-1]), 2)
        except:
            self.on_error('exit_order::create_order')

# -------------------------------
# EOF
# -------------------------------
