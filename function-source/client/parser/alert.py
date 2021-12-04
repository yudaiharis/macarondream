#import json

# -------------------------------
# AlertParser Class
# -------------------------------
class AlertParser:

    LongAlert = 1
    ShortAlert = 2
    LongExitAlert = 3
    ShortExitAlert = 4

    def __init__(self, title):
        self.result = 0
        self.entry_tp = 0.0
        self.entry_sl = 0.0
        self.trail_price = 0.0
        #self.amount = 0.0
        self.price = 0.0
        self.buy = False
        #self.entry = False
        self.title = title

    #def parse(self, message):
    #    pass

    #def get_result(self):
    #	return self.result

    def parse(self, request):
        param_dict = request.get_json()
        #param_dict = request
        message = param_dict['message']
        column = message.split(',')
        alert = param_dict['name']
        if alert == self.title:
            order = param_dict['action']
            position = float(param_dict['size'])
            self.price = float(param_dict['price'])
            self.entry_tp = float(column[0])
            self.entry_sl = float(column[1])
            self.trail_price = float(column[2])
            #self.amount = float(column[3])
            if position > 0:
                self.result = self.LongAlert
                self.buy = True
                return self.result
            elif position < 0:
                self.result = self.ShortAlert
                self.buy = False
                return self.result
            else:
                if order == 'buy':
                    self.result = self.ShortExitAlert
                    self.buy = False
                    return self.result
                elif order == 'sell':
                    self.result = self.LongExitAlert
                    self.buy = True
                    return self.result
                self.result = 0
            return self.result

# -------------------------------
# EOF
# -------------------------------