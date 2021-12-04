from ..client import Client
from ..consts import *

class MixApi(Client):
    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, first=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, first)

    '''
    获取用户 账户信息
    symbol: 合约交易对
    marginCoin: 保证金币种
    :return:
    '''
    def account(self, symbol, marginCoin):
        params = {}
        if symbol and marginCoin:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            return self._request_with_params(GET, MIX_ACCOUNT_V1_URL + '/account', params)
        else:
            return "pls check args"

    '''
    调整杠杆
    symbol: 合约交易对
    marginCoin: 保证金币种
    leverage: 杠杆倍数
    holdSide: 持仓方向 long 多仓 short 空仓  全仓时可以不传
    :return:
    '''
    def leverage(self, symbol, marginCoin, leverage, holdSide=''):
        params = {}
        if symbol and marginCoin:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["leverage"] = leverage
            params["holdSide"] = holdSide
            return self._request_with_params(POST, MIX_ACCOUNT_V1_URL + '/setLeverage', params)
        else:
            return "pls check args"

    '''
    调整保证金
    symbol: 合约交易对
    marginCoin: 保证金币种
    amount: 保证金金额  正数 增加 负数减少
    holdSide: 持仓方向 long 多仓 short 空仓  全仓时可以不传
    :return:
    '''
    def margin(self, symbol, marginCoin, amount, holdSide=''):
        params = {}
        if symbol and marginCoin:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["amount"] = amount
            params["holdSide"] = holdSide
            return self._request_with_params(POST, MIX_ACCOUNT_V1_URL + '/setMargin', params)
        else:
            return "pls check args"

    '''
    调整保证金模式
    symbol: 合约交易对
    marginCoin: 保证金币种
    marginMode: fixed 逐仓  crossed 全仓
    :return:
    '''
    def margin_mode(self, symbol, marginCoin, marginMode):
        params = {}
        if symbol and marginCoin:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["marginMode"] = marginMode
            return self._request_with_params(POST, MIX_ACCOUNT_V1_URL + '/setMarginMode', params)
        else:
            return "pls check args"

    '''
    设置持仓模式
    symbol: 合约交易对
    marginCoin: 保证金币种
    holdMode: 持仓模式 single_hold 单项持仓  double_hold双向持仓  默认双向
    :return:
    '''
    def position_mode(self, symbol, marginCoin, holdMode):
        params = {}
        if symbol and marginCoin and holdMode:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["holdMode"] = holdMode
            return self._request_with_params(POST, MIX_ACCOUNT_V1_URL + '/setPositionMode', params)
        else:
            return "pls check args"

    '''
    查询可开张数
    symbol: 合约交易对
    marginCoin: 保证金币种
    openPrice： 开仓价格
    openAmount: 开仓额度
    leverage: 杠杆倍数 默认20
    :return:
    '''
    def open_count(self, symbol, marginCoin, openPrice, openAmount, leverage=20):
        params = {}
        if symbol and marginCoin and openPrice and openAmount:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["openPrice"] = openPrice
            params["openAmount"] = openAmount
            params["leverage"] = leverage
            return self._request_with_params(POST, MIX_ACCOUNT_V1_URL + '/open-count', params)
        else:
            return "pls check args"

    '''
    获取账户信息列表
    productType: umcbl(USDT专业合约) dmcbl(混合合约) sumcbl(USDT专业合约模拟盘)  sdmcbl(混合合约模拟盘)
    :return:
    '''
    def accounts(self, productType):
        params = {}
        if productType:
            params['productType'] = productType
            return self._request_with_params(GET, MIX_ACCOUNT_V1_URL + '/accounts', params)
        else:
            return "pls check args"

    '''
    获取合约列表
    productType: umcbl(USDT专业合约) dmcbl(混合合约) sumcbl(USDT专业合约模拟盘)  sdmcbl(混合合约模拟盘)
    :return:
    '''
    def contracts(self, productType):
        params = {}
        if productType:
            params['productType'] = productType
        return self._request_with_params(GET, MIX_MARKET_V1_URL + '/contracts', params)

    '''
    获取深度数据
    symbol：合约交易对
    :return:
    '''
    def depth(self, symbol, limit='150'):
        params = {}
        if symbol and limit and type:
            params["symbol"] = symbol
            params["limit"] = limit
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/depth', params)
        else:
            return "pls check args"

    '''
    根据币对获取ticker信息
    symbol：合约交易对
    :return:
    '''
    def ticker(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/ticker', params)
        else:
            return "pls check args"

    '''
    获取全部ticker信息
    productType: umcbl(USDT专业合约) dmcbl(混合合约) sumcbl(USDT专业合约模拟盘)  sdmcbl(混合合约模拟盘)
    :return:
    '''
    def tickers(self,productType):
        params = {}
        if productType:
            params['productType'] = productType
        return self._request_with_params(GET, MIX_MARKET_V1_URL + '/tickers', params)

    '''
    获取实时成交
    symbol：合约交易对
    :return:
    '''
    def fills(self, symbol, limit=100):
        params = {}
        if symbol and limit:
            params["symbol"] = symbol
            params["limit"] = limit
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/fills', params)
        else:
            return "pls check args"

    '''
    获取 k 线信息
    params
    period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
    startTime: 开始时间
    endTime: 结束时间
    :return:
    '''
    def candles(self, symbol, granularity, startTime='', endTime=''):
        params = {}
        if symbol and granularity:
            params["symbol"] = symbol
            params["granularity"] = granularity
            params["startTime"] = startTime
            params["endTime"] = endTime
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/candles', params)
        else:
            return "pls check args"

    '''
    币种指数价格
    symbol：合约交易对
    :return:
    '''
    def index(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/index', params)
        else:
            return "pls check args"

    '''
    下一次结算时间
    symbol：合约交易对
    :return:
    '''
    def funding_time(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/funding-time', params)
        else:
            return "pls check args"

    '''
    合约标记价格
    symbol：合约交易对
    :return:
    '''
    def market_price(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/mark-price', params)
        else:
            return "pls check args"

    '''
    历史资金费率
    symbol：合约交易对
    pageSize: 查询条数
    pageNo: 查询页数
    nextPage: 是否查询下一页
    :return:F
    '''
    def history_fund_rate(self, symbol, pageSize=20, pageNo=1, nextPage=False):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            params["nextPage"] = nextPage
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/history-fundRate', params)
        else:
            return "pls check args"

    '''
    当前资金费率
    symbol：合约交易对
    :return:F
    '''
    def current_fund_rate(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/current-fundRate', params)
        else:
            return "pls check args"

    '''
    获取平台总持仓量
    symbol：合约交易对
    :return:
    '''
    def open_interest(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_MARKET_V1_URL + '/open-interest', params)
        else:
            return "pls check args"

    '''
    下单
    price: 限价时 为 必填  
    marginCoin: 保证金币种
    size: 限价时 为 数量  市价买 为额度 卖为数量
    side：open_long open_short close_long close_short
    orderType: limit(限价)  market(市价)
    timeInForceValue:normal(普通限价订单)   postOnly(只做maker,市价不允许使用这个)  ioc(立即成交并取消剩余)  fok(全部成交或立即取消)
    presetTakeProfitPrice: 预设止盈价格
    presetStopLossPrice： 预设止损价格
    :return:
    '''
    def place_order(self, symbol, marginCoin, size, side, orderType, price='', clientOrderId='', timeInForceValue='normal', presetTakeProfitPrice='', presetStopLossPrice=''):
        params = {}
        if symbol and marginCoin and side and orderType and marginCoin:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["price"] = price
            params["size"] = size
            params["side"] = side
            params["orderType"] = orderType
            params["timeInForceValue"] = timeInForceValue
            params["clientOrderId"] = clientOrderId
            params["presetTakeProfitPrice"] = presetTakeProfitPrice
            params["presetStopLossPrice"] = presetStopLossPrice
            return self._request_with_params(POST, MIX_ORDER_V1_URL + '/placeOrder', params)
        else:
            return "pls check args "

    '''
    批量下单
    price: 限价时 为 必填  
    marginCoin: 保证金币种
    order_data: 
    size: 限价时 为 数量  市价买 为额度 卖为数量
    side：open_long open_short close_long close_short
    orderType: limit(限价)  market(市价)
    timeInForceValue:normal(普通限价订单)   postOnly(只做maker,市价不允许使用这个)  ioc(立即成交并取消剩余)  fok(全部成交或立即取消)
    presetTakeProfitPrice: 预设止盈价格
    presetStopLossPrice： 预设止损价格
    :return:
    '''
    def batch_orders(self, symbol, marginCoin, order_data):
        params = {'symbol': symbol, 'marginCoin': marginCoin, 'orderDataList': order_data}
        return self._request_with_params(POST, MIX_ORDER_V1_URL + '/batch-orders', params)

    '''
    撤单
    :return:
    '''
    def cancel_orders(self, symbol, marginCoin, orderId):
        params = {}
        if symbol and orderId:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["orderId"] = orderId
            return self._request_with_params(POST, MIX_ORDER_V1_URL + '/cancel-order', params)
        else:
            return "pls check args "

    '''
    批量撤单
    orderIds: List 
    :return:
    '''
    def cancel_batch_orders(self, symbol, marginCoin, orderIds):
        if symbol and orderIds:
            params = {'symbol': symbol, 'marginCoin':marginCoin, 'orderIds': orderIds}
            return self._request_with_params(POST, MIX_ORDER_V1_URL + '/cancel-batch-orders', params)
        else:
            return "pls check args "

    '''
    获取订单信息
    :return:
    '''
    def detail(self, symbol, orderId):
        params = {}
        if symbol and orderId:
            params["symbol"] = symbol
            params["orderId"] = orderId
            return self._request_with_params(GET, MIX_ORDER_V1_URL + '/detail', params)
        else:
            return "pls check args "

    '''
    获取当前委托单
    :return:
    '''
    def current(self, symbol):
        params = {}
        if symbol:
            params["symbol"] = symbol
            return self._request_with_params(GET, MIX_ORDER_V1_URL + '/current', params)
        else:
            return "pls check args "

    '''
    获取历史委托
    isPre： 是否查询上一页
    :return:
    '''
    def history(self, symbol, startTime, endTime, pageSize, lastEndId='', isPre=False):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["startTime"] = startTime
            params["endTime"] = endTime
            params["pageSize"] = pageSize
            params["lastEndId"] = lastEndId
            params["isPre"] = isPre
            return self._request_with_params(GET, MIX_ORDER_V1_URL + '/history', params)
        else:
            return "pls check args "

    '''
    获取成交明细
    :return:
    '''
    def fills(self, symbol='', orderId=''):
        params = {}
        if symbol and orderId:
            params["symbol"] = symbol
            params["orderId"] = orderId
            return self._request_with_params(GET, MIX_ORDER_V1_URL + '/fills', params)
        else:
            return "pls check args "

    '''
    计划委托下单
    triggerPrice: 触发价格
    executePrice: 执行价格
    triggerType: 触发类型 fill_price market_price 
    marginCoin: 保证金币种
    size: 限价时 为 数量  市价买 为额度 卖为数量
    side：open_long open_short close_long close_short
    orderType: limit(限价)  market(市价)
    timeInForceValue:normal(普通限价订单)   postOnly(只做maker,市价不允许使用这个)  ioc(立即成交并取消剩余)  fok(全部成交或立即取消)
    presetTakeProfitPrice: 预设止盈价格
    presetStopLossPrice： 预设止损价格
    :return:
    '''
    def place_plan(self, symbol, marginCoin, size, side, orderType, triggerPrice, triggerType, executePrice='', clientOrderId='', timeInForceValue='normal', presetTakeProfitPrice='', presetStopLossPrice=''):
        params = {}
        if symbol and marginCoin and side and orderType and triggerPrice and triggerType:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["triggerPrice"] = triggerPrice
            params["executePrice"] = executePrice
            params["triggerType"] = triggerType
            params["size"] = size
            params["side"] = side
            params["orderType"] = orderType
            params["timeInForceValue"] = timeInForceValue
            params["clientOrderId"] = clientOrderId
            params["presetTakeProfitPrice"] = presetTakeProfitPrice
            params["presetStopLossPrice"] = presetStopLossPrice
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/placePlan', params)
        else:
            return "pls check args "

    '''
    修改计划委托
    triggerPrice: 触发价格
    executePrice: 执行价格
    triggerType: 触发类型 fill_price market_price 
    marginCoin: 保证金币种
    orderType: limit(限价)  market(市价)
    :return:
    '''
    def modify_plan(self, symbol, marginCoin, orderId, orderType, triggerPrice, triggerType, executePrice=''):
        params = {}
        if symbol and marginCoin and orderType and orderId and triggerType:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["orderId"] = orderId
            params["triggerPrice"] = triggerPrice
            params["executePrice"] = executePrice
            params["triggerType"] = triggerType
            params["orderType"] = orderType
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/modifyPlan', params)
        else:
            return "pls check args "

    '''
    修改计划委托预设止盈止损
    orderId：订单号
    triggerType: 触发类型 
    marginCoin: 保证金币种
    planType: 计划委托类型 normal_plan 普通计划 profit_plan止盈计划 loss_plan止损计划
    presetTakeProfitPrice: 预设止盈价格
    presetStopLossPrice： 预设止损价格
    :return:
    '''
    def modify_plan_preset(self, symbol, marginCoin, orderId, planType='normal_plan', presetTakeProfitPrice='', presetStopLossPrice=''):
        params = {}
        if symbol and marginCoin and orderId and planType:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["planType"] = planType
            params["orderId"] = orderId
            params["presetTakeProfitPrice"] = presetTakeProfitPrice
            params["presetStopLossPrice"] = presetStopLossPrice
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/modifyPlanPreset', params)
        else:
            return "pls check args "

    '''
    修改计划委托预设止盈止损
    orderId：订单号
    triggerPrice: 触发价格
    marginCoin: 保证金币种
    :return:
    '''
    def modify_tpsl_plan(self, symbol, marginCoin, orderId, triggerPrice ):
        params = {}
        if symbol and marginCoin and orderId and triggerPrice:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["orderId"] = orderId
            params["triggerPrice"] = triggerPrice
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/modifyTPSLPlan', params)
        else:
            return "pls check args "

    '''
    止盈止损下单
    目前止盈止损下单  只支持市价 触发类型为成交价格
    symbol: 交易对名称
    marginCoin: 保证金币种
    orderId: 订单id 
    planType: 订单类型   profit_plan 止盈计划  loss_plan止损计划
    holdSide: 持仓方向 long 多仓  short 空仓
    :return:
    '''
    def place_tpsl(self, symbol, marginCoin, triggerPrice, planType, holdSide ):
        params = {}
        if symbol and marginCoin and planType and holdSide and triggerPrice:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["planType"] = planType
            params["holdSide"] = holdSide
            params["triggerPrice"] = triggerPrice
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/placeTPSL', params)
        else:
            return "pls check args "


    '''
    计划委托(止盈止损)撤单
    symbol: 交易对名称
    marginCoin: 保证金币种
    orderId: 订单id 
    planType: 订单类型  normal_plan 计划委托  profit_plan 止盈计划  loss_plan止损计划
    :return:
    '''
    def cancel_plan(self, symbol, marginCoin, orderId, planType):
        params = {}
        if symbol and marginCoin and planType and orderId:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            params["planType"] = planType
            params["orderId"] = orderId
            return self._request_with_params(POST, MIX_PLAN_V1_URL + '/cancelPlan', params)
        else:
            return "pls check args "

    '''
    获取当前计划委托
    isPlan: 是否查询计划委托  plan计划委托   profit_loss止盈止损
    :return:
    '''
    def current_plan(self, symbol, isPlan='plan'):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["isPlan"] = isPlan
            return self._request_with_params(GET, MIX_PLAN_V1_URL + '/currentPlan', params)
        else:
            return "pls check args "

    '''
    获取历史计划委托
    isPre： 是否查询上一页
    isPlan: 是否查询计划委托  plan计划委托   profit_loss止盈止损
    :return:
    '''
    def history_plan(self, symbol, startTime, endTime, pageSize, lastEndId='', isPre=False, isPlan='plan'):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["startTime"] = startTime
            params["endTime"] = endTime
            params["pageSize"] = pageSize
            params["lastEndId"] = lastEndId
            params["isPre"] = isPre
            params["isPlan"] = isPlan
            return self._request_with_params(GET, MIX_PLAN_V1_URL + '/historyPlan', params)
        else:
            return "pls check args "

    '''
    获取用户单个持仓信息
    :return:
    '''
    def single_position(self, symbol, marginCoin):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["marginCoin"] = marginCoin
            return self._request_with_params(GET, MIX_POSITION_V1_URL + '/singlePosition', params)
        else:
            return "pls check args"

    '''
    获取用户单个持仓信息
    productType: umcbl(USDT专业合约) dmcbl(混合合约) sumcbl(USDT专业合约模拟盘)  sdmcbl(混合合约模拟盘)
    :return:
    '''
    def all_position(self, productType, marginCoin):
        params = {}
        if productType:
            params["productType"] = productType
            params["marginCoin"] = marginCoin
            return self._request_with_params(GET, MIX_POSITION_V1_URL + '/allPosition', params)
        else:
            return "pls check args"

    '''
    交易员平仓
    symbol： 交易对名称
    trackingNo: 跟踪订单号
    :return:
    '''
    def close_track_order(self, symbol, trackingNo):
        params = {}
        if symbol and trackingNo:
            params["symbol"] = symbol
            params["trackingNo"] = trackingNo
            return self._request_with_params(POST, MIX_TRACE_V1_URL + '/closeTrackOrder', params)
        else:
            return "pls check args "

    '''
    交易员获取当前带单
    symbol: 交易对名称
    productType: umcbl(USDT专业合约) dmcbl(混合合约) sumcbl(USDT专业合约模拟盘)  sdmcbl(混合合约模拟盘)
    pageNo： 从1开始
    :return:
    '''
    def current_track(self, symbol, productType, pageSize=20, pageNo=1):
        params = {}
        if symbol:
            params["symbol"] = symbol
            params["productType"] = productType
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            return self._request_with_params(GET, MIX_TRACE_V1_URL + '/currentTrack', params)
        else:
            return "pls check args "

    '''
    交易员获取当前带单
    symbol: 交易对名称
    startTime: 开始时间
    endTime: 结束时间
    pageSize: 查询条数
    pageNo: 查询页数
    :return:
    '''
    def history_track(self, startTime, endTime, pageSize=100, pageNo=1):
        params = {}
        if startTime and endTime:
            params["startTime"] = startTime
            params["endTime"] = endTime
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            return self._request_with_params(GET, MIX_TRACE_V1_URL + '/historyTrack', params)
        else:
            return "pls check args "

    '''
    交易员分润汇总
    :return:
    '''
    def summary(self):
        return self._request_without_params(GET, MIX_TRACE_V1_URL + '/summary')

    '''
    交易员分润汇总(按结算币种)
    :return:
    '''
    def profit_settle_margin_coin(self):
        return self._request_without_params(GET, MIX_TRACE_V1_URL + '/profitSettleTokenIdGroup')

    '''
    交易员分润汇总(按日期)
    :return:
    '''
    def profit_date_group(self, pageSize, pageNo):
        params = {}
        if pageSize and pageNo:
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            return self._request_with_params(GET, MIX_TRACE_V1_URL + '/profitDateGroupList', params)
        else:
            return "pls check args "

    '''
    交易员历史分润明细
    :return:
    '''
    def profit_date_detail(self, marginCoin, date, pageSize, pageNo):
        params = {}
        if marginCoin and date and pageSize and pageNo:
            params["marginCoin"] = marginCoin
            params["date"] = date
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            return self._request_with_params(GET, MIX_TRACE_V1_URL + '/profitDateList', params)
        else:
            return "pls check args "

    '''
    交易员待分润明细
    :return:
    '''
    def wait_profit_detail(self, pageSize, pageNo):
        params = {}
        if pageSize and pageNo:
            params["pageSize"] = pageSize
            params["pageNo"] = pageNo
            return self._request_with_params(GET, MIX_TRACE_V1_URL + '/waitProfitDateList', params)
        else:
            return "pls check args "
