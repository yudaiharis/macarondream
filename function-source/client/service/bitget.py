import ccxt
from retry import retry
from ccxt.base.errors import ExchangeNotAvailable
from client.service.exchange import ExchangeService
from client.service.bitgetSDK.mix.mix_api import MixApi
import math
import time

# -------------------------------
# BitgetService Class
# -------------------------------
class BitgetService(ExchangeService):
    
    def __init__(self, symbol, config, exchange, on_error):
        super().__init__(config, exchange, on_error)
        #self.bitget = ccxt.bitget({
        #    'apiKey': config.get('settings', 'API_KEY'), 
        #    'secret': config.get('settings', 'API_SECRET'), 
        #    'password': config.get('settings', 'API_PASSWORD'), 
        #    'timeout': 100000,
        #    'enableRateLimit': False,
        #    'options':{
        #        'defaultType':'swap'
        #    }
        #})
        #self.bitget.verbose = config.getboolean('settings', 'DEBUG') # debugmode 
        #self.bitget.load_markets()
        #self.symbol = self.find_symbol(self.bitget, symbol)
        self.bitget_sdk = MixApi(
            config.get('settings', 'API_KEY'), 
            config.get('settings', 'API_SECRET'), 
            config.get('settings', 'API_PASSWORD'), 
            use_server_time=True, 
            first=False,
        )
        if config.getboolean('settings', 'TESTNET'):
            self.producttype = 'sumcbl'
            self.basecoin = 'SBTC'
        else:
            self.producttype = 'umcbl'
            self.basecoin = 'BTC'
        contracts = self.bitget_sdk.contracts(self.producttype)['data']
        self.symbol = [x['symbol'] for x in contracts if x['baseCoin'] == self.basecoin][0]
        self.margincoin = [x['supportMarginCoins'] for x in contracts if x['baseCoin'] == self.basecoin][0][0]
        self.bitget_sdk.leverage(self.symbol, self.margincoin, self.flexible_leverage, holdSide='long')
        self.balance = round(float(self.__get_balance()), 2)
        self.trader = config.get('settings', 'TRADER')


    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __get_balance(self):
        #balances = self.bitget.fetch_balance()
        balances = self.bitget_sdk.account(self.symbol, self.margincoin)
        return balances['data']['available']

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __get_best_price(self):
        ticker = self.bitget.fetch_ticker(self.symbol)
        return (float)(ticker['bid']), (float)(ticker['ask'])

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __create_entry_order(self, buy):
        self.side = 'open_long' if buy else 'open_short'
        #type = '1' if buy else '2'
        #params = {
        #    'type' : type, 
        #    'presetTakeProfitPrice' : self.entry_tp,
        #    'presetStopLossPrice' : self.entry_sl, 
        #}
        if self.fixed_lot:
            self.entry_amount = self.fixed_lot_size
        else:
            self.entry_amount = round(self.balance / 1000 * self.flexible_lot_percent, 3)
            if self.entry_amount < 0.001:
                self.entry_amount = 0.001
        #self.bitget.create_order(self.symbol, 'market', self.side, amount, params=params)
        self.bitget_sdk.place_order(
            self.symbol, 
            self.margincoin, 
            size=self.entry_amount, 
            side=self.side, 
            orderType='market', 
            price='', 
            timeInForceValue='normal', 
            presetTakeProfitPrice=self.entry_tp, 
            presetStopLossPrice=self.entry_sl
        )
        return

    @retry(ExchangeNotAvailable, tries=100, delay=0.25)
    def __create_exit_order(self, buy): # (self, market_id, trackingNo):
        if self.trader and self.producttype == 'umcbl':
            track = self.bitget_sdk.current_track(self.symbol, self.producttype, pageSize=100, pageNo=1)
            self.bitget_sdk.close_track_order(self.symbol, trackingNo=track['data'][0]['trackingNo'])
        else:
            self.side = 'close_long' if buy else 'close_short'
            self.bitget_sdk.place_order(
                self.symbol, 
                self.margincoin, 
                size=self.exit_amount, 
                side=self.side, 
                orderType='market', 
                price='', 
                timeInForceValue='normal'
            )        
        #self.bitget_sdk.close_track_order(market_id, trackingNo)
        #self.bitget.create_order(self.symbol, 'market', self.side, amount, params)
        return

    def fetch_positions(self):     
        orders = self.bitget_sdk.all_position(self.producttype, self.margincoin)['data']
        #order = [x['openDelegateCount'] for x in orders if x['symbol'] == self.symbol]
        order = [x['total'] for x in orders if x['symbol'] == self.symbol]
        if len(order) <= 1:
            self.exit_amount = 0.0
            return False
        elif order[0] != '0' or order[1] != '0' :
            self.exit_amount = order[0] if order[0] != '0' else order[1]
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
            trades = self.bitget_sdk.history(self.symbol, startTime=starttime, endTime=endtime, pageSize=20, lastEndId='',isPre=False)
            self.closed_pnl = trades['data']['orderList'][0]['totalProfits']
        except:
            self.on_error('exit_order::create_order')

# -------------------------------
# EOF
# -------------------------------