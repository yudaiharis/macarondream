import ccxt
import random
from retry import retry
from ccxt.base.errors import ExchangeNotAvailable
from client.service.exchange import ExchangeService

# -------------------------------
# BybitService Class
# -------------------------------
class BybitService(ExchangeService):
    
    def __init__(self, symbol, config, exchange, on_error):
        super().__init__(config, exchange, on_error)
        self.bybit = ccxt.bybit({
            'apiKey': config.get('settings', 'API_KEY'), 
            'secret': config.get('settings', 'API_SECRET'), 
            'timeout': 100000,
        }) 
        self.bybit.set_sandbox_mode(config.getboolean('settings', 'TESTNET')) # debugmode
        self.bybit.verbose = config.getboolean('settings', 'DEBUG')
        self.bybit.load_markets()
        #self.symbol = self.find_symbol(self.bybit, symbol)
        self.symbol = symbol
        params = {
            'buy_leverage' : random.randint(1, 100),
            'sell_leverage' : random.randint(1, 100)
        }
        self.bybit.set_leverage(leverage=True, symbol=self.symbol, params=params)
        params = {
            'buy_leverage' : self.flexible_leverage,
            'sell_leverage' : self.flexible_leverage
        }
        self.bybit.set_leverage(leverage=True, symbol=self.symbol, params=params)
        self.balance = round(float(self.__get_balance()), 2)

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __get_balance(self):
        balance = self.bybit.fetch_balance({'coin': 'USDT'})
        return balance['info']['result']['USDT']['available_balance']

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __get_best_price(self):
        ticker = self.bybit.fetch_ticker(self.symbol)
        #ticker = self.bybit.fetch_tickers()[self.symbol]
        return (float)(ticker['info']['bid_price']), (float)(ticker['info']['ask_price'])

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __create_entry_order(self, buy):
        self.side = 'Buy' if buy else 'Sell'
        params = {'take_profit' : self.entry_tp, 'stop_loss' : self.entry_sl}
        if self.fixed_lot:
            self.entry_amount = self.fixed_lot_size
        else:
            self.entry_amount = round(self.balance / 1000 * self.flexible_lot_percent, 3)
            if self.entry_amount < 0.001:
                self.entry_amount = 0.001
        self.bybit.create_order(self.symbol, 'market', self.side, self.entry_amount, params=params)
            #order = self.bybit.private_linear_post_order_create({
            #    'symbol' : self.symbol, 
            #    'order_type' : 'Market', 
            #    'side' : self.side, 
            #    'qty' : amount, 
            #    'price' : price, 
            #    'time_in_force' : 'GoodTillCancel'
            #})
        return

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __create_exit_order(self, buy):
        self.side = 'Sell' if buy else 'Buy'
        params = {'reduce_only' : True} 
        self.bybit.create_order(self.symbol, 'market', self.side, self.exit_amount, params=params)
            #order = self.bybit.private_linear_post_order_create({
            #    'symbol' : 'BTCUSDT', 
            #    'order_type' : 'Market', 
            #    'side' : self.side, 
            #    'qty' : amount, 
            #    'price' : price, 
            #    'time_in_force' : 'GoodTillCancel',
            #    'reduce_only' : True
            #})
        return

    def fetch_positions(self):     
        orders = self.bybit.fetch_positions()          
        order = [x['data']['size'] for x in orders if x['data']['symbol'] == self.symbol]
        print('\norder={}'.format(order))
        if len(order) <= 1:
            self.exit_amount = 0.0
            return False
        elif order[0] != '0' or order[1] != '0' :
            self.exit_amount = order[0] if order[0] != '0' else order[1]
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
            trades = self.bybit.private_linear_get_trade_closed_pnl_list({
                'symbol' : self.symbol
            })
            self.closed_pnl = round(float(trades['result']['data'][0]['closed_pnl']), 2)
        except:
            self.on_error('exit_order::create_order')

# -------------------------------
# EOF
# -------------------------------
