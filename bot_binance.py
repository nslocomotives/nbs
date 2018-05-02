from binance.client import Client
import get_config
import time
import database

cfg = get_config.cfg
api_key = cfg['binance']['key']
api_secret = cfg['binance']['secret']
tSymbols = cfg['binance']['tradedSymbols']

client = Client(api_key, api_secret)
exchange= 'binance'

def get_openOrders():
    openOrders = client.get_open_orders()
    #display open orders
    #for o in openOrders:
    #    print (o['symbol'] + ':' + o['price'])
    return(openOrders)

def get_funds(coins):
    #gets the balance of the coin
    balance = {}
    for c in coins:
      balance[c] = client.get_asset_balance(asset=c)
    return(balance)

def get_account_info():
    info = client.get_account()
    assets = []
    
    #for key in info:
    #  print (key)

    # get the balances if you have more than 0 then we care about it
    for coin in info['balances']:
        # work out total balance of coin
        coin['free'] = float(coin['free'])
        coin['locked'] = float(coin['locked'])
        coin['total'] = coin['free'] + coin['locked']
        if coin['total'] > 0:
          #debug info
          #print(coin['asset'], total)
          assets.append(coin)
        if coin['asset'] == 'ETH':
          coin['symbol'] = coin['asset'] + 'BTC'
        else :
          coin['symbol'] = coin['asset'] + 'ETH'
          
    return(assets)

def decimal_formatter(number):
    return format(number, '.8f')

def get_total_deposits():
    deposits = client.get_deposit_history()
    totaldeps = {}
    totaldeps['ETH'] = 0
    totaldeps['BTC'] = 0
    totaldeps['BNB'] = 0
    for deposit in deposits['depositList']:
        totaldeps[deposit['asset']] += float(deposit['amount'])

    
    return(totaldeps)
    
def get_total_balance(deposits, assets):
    ethTotal = 0
    totalbal = {}
    for a in assets:
      try:
        ticker = client.get_ticker(symbol=a['symbol'])
      except:
        pass
      if ticker:
        if a['symbol'] != 'BNBETH':
          ethval = float(a['total']) * float(ticker['lastPrice'])
          if a['symbol'] == 'ETHBTC':
            ethval = float(a['total'])
          ethTotal += ethval
        else:
          bnbTotal = float(a['total'])

    totalbal['eth'] = ethTotal
    totalbal['bnb'] = bnbTotal
    
    return(totalbal)
    
def bot_hello():

    assets = get_account_info()

    print('Hello nbs-binace-bot says...')
    print('============================')
    print('')
    print('Original Deposit')
    deposits = get_total_deposits()
    for key, value in deposits.items():
      print (key, decimal_formatter(value))
    print('')
    totals = get_total_balance(deposits, assets)
    print('')
    print ('ETH Total =' + decimal_formatter(totals['eth']))
    print ('BNB Total =' + decimal_formatter(totals['bnb']))

def check_orders(prevOrders):
    orders = get_openOrders()
    closedOrders = [item for item in prevOrders if item not in orders]
    return(orders, closedOrders)

def get_all_trades():
    trades = {}
    for i in tSymbols:
        #print(i)
        lastTradeId = database.getLastTradeId(exchange,i)
        #print(lastTradeId)
        if lastTradeId == 'no trades':
            trades[i]   = client.get_my_trades(symbol=i)
        else:
            trades[i]   = client.get_my_trades(symbol=i, fromId=lastTradeId)
            if trades[i][0]['id'] == lastTradeId:
                trades[i].pop(0)
             
                
    return(trades)
    
def update_trades_db():
    trades = get_all_trades()
    #print(trades)
    for symbol, data in trades.items():
        database.insertTrades(data, symbol, exchange)
    return()

