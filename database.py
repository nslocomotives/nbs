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
