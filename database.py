import pymysql.cursors
import get_config

cfg = get_config.cfg['mysql']

dbConfig = {
  'user': cfg['user'],
  'password': cfg['password'],
  'host': cfg['host'],
  'database': cfg['database'],
  'cursorclass' : pymysql.cursors.DictCursor
}

def insertTransaction(data):
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT COUNT(id) as tally FROM transaction WHERE accountnumber=%s AND date=%s AND description=%s AND amount=%s AND ballance=%s"
          insert_sql = "INSERT INTO transaction(accountnumber, date, description, amount, ballance) VALUES (%s, %s, %s, %s, %s)"
          # Insert records
          for row in data:
            cursor.executemany(select_sql,[(row['accountnumber'],row['Date'],row['Description'],row['Amount'],row['Balance'])])
            check = cursor.fetchone()
            if check['tally'] > 0:
                print('Oops Duplicate transaction' + ' : ' + row['accountnumber'] + ' : ' + row['Date'] + ' : ' + row['Description'] + ' : ' + row['Amount'] + ' : ' + row['Balance'])
            else:
                cursor.executemany(insert_sql,[(row['accountnumber'],row['Date'],row['Description'],row['Amount'],row['Balance'])])
                cnx.commit()
  finally:
    cnx.close()

def insertTrades(data, symbol, exchange):
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT COUNT(id) as tally FROM trades WHERE exchange=%s AND symbol=%s AND exchangeId=%s AND orderId=%s"
          insert_sql = "INSERT INTO trades(exchange, symbol, exchangeId, orderId, price, qty, commission, commissionAsset, time, isBuyer, isMaker, isBestMatch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
          # Insert records
          for row in data:
            cursor.executemany(select_sql,[(exchange,symbol,row['id'],row['orderId'])])
            check = cursor.fetchone()
            if check['tally'] > 0:
                print('Oops Duplicate trade' + ' : ' + exchange + ' : ' + str(row['id']) + ' : ' + str(row['orderId']) + ' : ' + symbol + ' : ' + str(row['price']))
            else:
                cursor.executemany(insert_sql,[(exchange,symbol,row['id'],row['orderId'],row['price'],row['qty'],row['commission'],row['commissionAsset'],row['time'],row['isBuyer'],row['isMaker'],row['isBestMatch'])])
                cnx.commit()
  finally:
    cnx.close()
	
def getLastTradeId(exchange, symbol):
  # a function to get the most recent exchangeId for the trade symbol and exchange
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT MAX(exchangeId) as exchangeId FROM trades WHERE exchange=%s AND symbol=%s"
          # get the data
          cursor.executemany(select_sql,[(exchange,symbol)])
          lastTradeId = cursor.fetchone()
          lastTradeId = lastTradeId['exchangeId']
          #print(lastTradeId)
          if lastTradeId:
	          result = lastTradeId
          else: 
              result = 'no trades'
  finally:
    cnx.close()
  return (result)
  
def getCategory(isIncome):
  # a function to get the catagories
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT id, name from category where isIncome=%s"
          # get the data
          cursor.executemany(select_sql,[(isIncome)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getSubCategory(lnk):
  # a function to get the catagories by category link
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT id, name from subCategory where category_lnk=%s"
          # get the data
          cursor.executemany(select_sql,[(lnk)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getSubCategoryById(lnk):
  # a function to get the sub catagory by ID to return the name.
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT name from subCategory where id=%s"
          # get the data
          cursor.executemany(select_sql,[(lnk)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getAccounts():
  # a function to get the accounts in the database
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT * from accounts"
          # get the data
          cursor.execute(select_sql)
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getTransactionDataByAccount(accountnumber, startDate, endDate):
  # a function to get transactions based on account number
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT * from transaction where accountnumber=%s AND date BETWEEN %s AND %s"
          # get the data
          cursor.executemany(select_sql, [(accountnumber, startDate, endDate)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getTransactionData():
  # a function to get all transactions
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT * from transaction"
          # get the data
          cursor.execute(select_sql)
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getBal(accountnumber, date):
  # a function to get opening and closing balance based on account number and month
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT id, date, balance from transaction where accountnumber=%s AND date <= %s ORDER BY DATEDIFF( date, %s ) DESC LIMIT 1"
          # get the data
          cursor.executemany(select_sql, [(accountnumber, date, date)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getAccountNames(AccType):
  # a function to get a list of accounts by type
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT id, accountname from accounts where accountType IN (%s)"
          # get the data
          print (AccType)
          cursor.executemany(select_sql, [(AccType)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

def getAssets(date):
  # a function to get the list of assets we care about for a given month.
  # given the date, we will list the most recent value inserted for asset by name, and also filter out an asset sold before the given date.
  cnx = pymysql.connect(**dbConfig)
  try:
      with cnx.cursor() as cursor:
          select_sql = "SELECT name, value FROM assets ast1 WHERE ast1.insertDate = (SELECT max(ast2.insertDate) FROM assets ast2	WHERE ast2.name = ast1.name AND id IN ( SELECT id FROM assets WHERE insertDate < %s)) AND ast1.soldDate IS NULL"
          # get the data
          cursor.executemany(select_sql, [(date)])
          result = cursor.fetchall()
  finally:
    cnx.close()
  return (result)

