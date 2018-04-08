import glob
import re
import csv

from datetime import datetime

def extract_basename(path):
  # Extracts basename of a given path. Should Work with any OS Path on any OS
  basename = re.search(r'[^\\/]+(?=[\\/]?$)', path)
  if basename:
    return basename.group(0)

def process_file(path, typeFlag, accountNumber):
  # Collects the data from the CSV file according to the identified type and
  # pushes the data into an array.
  results = []
  with open(path) as File:
      data = csv.DictReader(File)
      for row in data:
          row['accountnumber'] = accountNumber
          row['Date'] = datetime.strptime(row['Date'], '%d/%m/%Y').strftime('%Y-%m-%d')
          results.append(row)
      #results = data
  return(results)

def identify_file(p, f):
  #find out if First Direct File (has "_" in it)
  if f.find('_') >= 0:
      str1 = f.find('_')
      str2 = str1 + 1
      date = f[:str1] #date file generated from filename
      a = f[str2:]
      str3 = a.find('.')
      a = a[:str3] #set account number from file name
      Flag = 'First Direct' #Type Flag for bank
  else:
      date = '00000000'
      a = 'UNKNOWN'
      Flag = 'UNKNOWN'
  return(Flag, date, a)

def statement(statementDir):
  # ===Start of Program ===#

  # find all csv files and list them
  csvFilesStr = statementDir + "*.csv"
  csvFiles = glob.glob(csvFilesStr)

  for p in csvFiles:
    print(p)
    f = extract_basename(p)
    (Flag, date, accountNumber) = identify_file(p, f)
    #log out details of file
    print('First Direct File: "' + f +'"')
    print('File generated on: ' + date)
    print('Account Number: ' + accountNumber)
    if Flag != 'UNKNOWN':
        #start work on the file
        results = process_file(p, Flag, accountNumber)
        #for row in results:
        #  print(row['accountnumber'],row['Date'],row['Description'],row['Amount'],row['Balance'])
        return(results)
    else:
        #log out not able to work the file
        print('Unknown File unable to parse')


