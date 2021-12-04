
# -------------------------------
# ExchangeService Class
# -------------------------------
class ExchangeService:
    
    def __init__(self, config, exchange, on_error):
        self.exchange = exchange
        self.alert = ''
        self.buy = False
        self.side = ''
        self.entry = False
        self.entry_tp = 0
        self.entry_sl = 0
        self.trail_price = 0
        self.price = 0
        self.entry_amount = 0.0
        self.exit_amount = 0.0
        self.balance = 0.0
        self.closed_pnl = 0.0
        self.fixed_lot = config.getboolean('settings', 'FIXED_LOT')
        self.fixed_lot_size = config.getfloat('settings', 'FIXED_LOT_SIZE')
        self.flexible_leverage = int(config.getfloat('settings', 'FLEXIBLE_LEVERAGE'))
        self.flexible_lot_percent = config.getfloat('settings', 'FLEXIBLE_LOT_PERCENT')
        self.on_error = on_error
                
    def find_symbol(self, exchange, raw_symbol):
        if raw_symbol in exchange.markets_by_id:
            market = exchange.markets_by_id[raw_symbol]
            return market['symbol']
        return raw_symbol
        
# -------------------------------
# EOF
# -------------------------------
