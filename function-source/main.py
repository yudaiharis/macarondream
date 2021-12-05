import os
import sys
import time
import configparser
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from client.line import Linenotify
from client.twitter import Twitternotify
from client.parser.alert import AlertParser
from client.service.bybit import BybitService
from client.service.bitget import BitgetService
from client.service.binance import BinanceService
from client.wrapper.errors import MaintenanceError
from client.wrapper.errors import OverloadedError

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, 'setting', 'setting.ini')
config = configparser.ConfigParser()
config.read(file_path, 'utf_8_sig')
exchange = config.get('settings', 'EXCHANGE')
symbol = config.get('settings', 'SYMBOL')
line_notify_is = config.getboolean('settings', 'LINE_NOTIFY')
line_notify_token = config.get('settings', 'LINE_NOTIFY_TOKEN')
line_notify_tag = '[' + config.get('settings', 'LINE_NOTIFY_TAG') + ']'
trading_view_alert = config.get('settings', 'TRADING_VIEW_ALERT')
twitter_notify_is = config.getboolean('settings', 'TWITTER_NOTIFY')
twitter_api_key = config.get('settings', 'TWITTER_API_KEY')
twitter_api_secret = config.get('settings', 'TWITTER_API_SECRET')
twitter_token = config.get('settings', 'TWITTER_ACCESS_TOKEN')
twitter_token_secret = config.get('settings', 'TWITTER_ACCESS_TOKEN_SECRET')
tv_is = config.getboolean('settings', 'SCREENSHOT')
tv_dir = config.get('settings', 'TRADING_VIEW_DIR')
tv_fqdn = 'https://jp.tradingview.com/chart/'
if tv_is:
    tv_url = tv_fqdn + tv_dir
else:
    tv_url = ''


def push_message(push, notify, *lines):
    print('-------------------------------')
    for line in lines:
        print(line)
    print('-------------------------------')
    if push:
        body = (line_notify_tag,) + lines
        notify.send(*body)

def unknown_error_handling(log):
    ex, ms, _ = sys.exc_info()
    line1 = log
    line2 = 'unknown error {0}'.format(ex)
    line3 = '{0}'.format(ms)
    push_message(True, line1, line2, line3)
    sys.exit()

if exchange == 'Bybit':
    service = BybitService(symbol, config, exchange, unknown_error_handling)
elif exchange == 'Bitget':
    service = BitgetService(symbol, config, exchange, unknown_error_handling)
elif exchange == 'Binance':
    service = BinanceService(symbol, config, exchange, unknown_error_handling)
parser = AlertParser(trading_view_alert)
line_notify = Linenotify(line_notify_token)
twitter_notify = Twitternotify(twitter_api_key, twitter_api_secret, twitter_token, twitter_token_secret, exchange)

def main(request):
    try:
        alert = parser.parse(request) # AlertParser.result==0
        print('alert: {}'.format(alert))
        service.alert = parser.title
        service.entry_tp = round(parser.entry_tp)
        service.entry_sl = round(parser.entry_sl)
        service.trail_price = round(parser.trail_price)
        service.price = round(parser.price)
        service.buy = parser.buy
        print('service.buy: {}'.format(service.buy))
        service.entry = service.fetch_positions()
        print('service.entry: {}'.format(service.entry))
        if alert == AlertParser.LongAlert: # AlertParser.result==1
            if not service.entry:
                service.entry_order(True)
                notify(True)
            elif service.buy:
                service.exit_order(False)
                notify(False)            
                service.entry_order(True)
                notify(True)
        elif alert == AlertParser.ShortAlert: # AlertParser.result==2
            if not service.entry:
                service.entry_order(False)
                notify(True)
            elif not service.buy:
                service.exit_order(True)
                notify(False)
                service.entry_order(False)
                notify(True)
        elif alert == AlertParser.LongExitAlert: # AlertParser.result==3
            service.exit_order(True)
            notify(False)
        elif alert == AlertParser.ShortExitAlert: # AlertParser.result==4
            service.exit_order(False)
            notify(False)
        return ('Success!', 200, {})
    except MaintenanceError:
        time.sleep(10.0)
        return ('Error!', 500, {})
    except OverloadedError:
        time.sleep(5.0)
        return ('Error!', 500, {})

def notify(entry):
    now = datetime.now(timezone(timedelta(hours=9)))
    if entry:
        line1 = 'Exchange : {0}'.format(service.exchange)
        line2 = 'Alert : {0}'.format(service.alert)
        line3 = 'entry : {0}'.format(service.side)
        line4 = 'amount : {0} BTC'.format(service.entry_amount)
        line5 = 'price : ${0}'.format(service.price)
        line6 = 'takeprofit: ${0}'.format(service.trail_price)
        line7 = 'stoploss: ${0}'.format(service.entry_sl)
        line8 = 'balance : ${0}'.format(service.balance)
        line9 = 'time : {0}UTC+9'.format(now.strftime("%Y/%m/%d %H:%M:%S"))
        line10 = tv_url
        push_message(line_notify_is, line_notify, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10)
        push_message(twitter_notify_is, twitter_notify, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10)
    else:
        line1 = 'Exchange : {0}'.format(service.exchange)
        line2 = 'Alert : {0}'.format(service.alert)
        line3 = 'entry : position close'
        line4 = 'price : ${0}'.format(service.price)
        line5 = 'balance : ${0}'.format(service.balance)
        line6 = 'closed PNL : ${0}'.format(service.closed_pnl)
        line7 = 'time : {0}UTC+9'.format(now.strftime("%Y/%m/%d %H:%M:%S"))
        line8 = tv_url
        push_message(line_notify_is, line_notify, line1, line2, line3, line4, line5, line6, line7, line8)
        push_message(twitter_notify_is, twitter_notify, line1, line2, line3, line4, line5, line6, line7, line8)

# debug
#if __name__ == '__main__':
#    request = {"name":"target03","action":"buy","size":"1","price":"65000","message":"70000.3,30000.2,68000.1"}
#    main(request)
#    print('Finish !')