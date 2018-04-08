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
          sql = "INSERT INTO transaction(accountnumber, date, description, amount, ballance) VALUES (%s, %s, %s, %s, %s)"
          # Insert records
          for row in data:
            cursor.executemany(sql,[(row['accountnumber'],row['Date'],row['Description'],row['Amount'],row['Balance'])])
            cnx.commit()
  finally:
    cnx.close()
