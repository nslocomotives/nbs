from openpyxl import Workbook
from openpyxl.styles import Font, Fill
import database

wb = Workbook()

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
incomeCats=database.getCategory(1)
subcat={}

for i in incomeCats:
    subcat[i['name']]=database.getSubCategory(i['id'])
for i in incomeCats:
    print(i['name'])
    for j in subcat[i['name']]:
        print(j['name'])
        
houseExpenses=['Lodging Rent',
               'Lodging',
               'Lodging Tax (council)',
               'Lodging Utitlities',
               'Lodging Maintence',
               'Lodging Insurance',
               'Lodging Other']
djExpenses=['DJ Software',
            'DJ Insurance',
            'DJ Equipment',
            'DJ Other']
personalExpenses=['Shopping',
                  'Clothing',
                  'Entertainment',
                  'Crypto Investment',
                  'Dating',
                  'Eating/drinking Out',
                  'Birthdays and Christmas',
                  'Car Maintenance',
                  'Fuel',
                  'Child Maintence',
                  'FD Loan',
                  'Hitachi Loan',
                  'Mobile Phone',
                  'Life Insurance',
                  'TV License',
                  'Bank Charges',
                  'Debt repayment',
                  'Other Expenses']
earnedIncome=['wages',
              'DJ Income',
              'Ebay Sales',
              'Loan Capitol',
              'Loan repayment Refund',
              'Other']
pasiveIncome=['Lodging Income',
              'Buisness',
              'Passive Other']
portfolioIncome=['Interest',
                 'Crypto Withdrawal',
                 'Dividends',
                 'Royalties']
expenses=houseExpenses+djExpenses+personalExpenses
income=earnedIncome+pasiveIncome+portfolioIncome

# grab the active worksheet and create other worksheets and give them names
wsO = wb.active
wsO.title = "Overview"
wsB = wb.create_sheet("Budget")
wsJan = wb.create_sheet("Jan")
wsFeb = wb.create_sheet("Feb")
wsMar = wb.create_sheet("Mar")
wsApr = wb.create_sheet("Apr")
wsMay = wb.create_sheet("May")
wsJun = wb.create_sheet("Jun")
wsJul = wb.create_sheet("Jul")
wsAug = wb.create_sheet("Aug")
wsSep = wb.create_sheet("Sep")
wsOct = wb.create_sheet("Oct")
wsNov = wb.create_sheet("Nov")
wsDec = wb.create_sheet("Dec")

#set starting rows
wsOrow = 2
wsBrow = 2
wsMrow = 2

#create the budget header
wsB['A' + str(wsBrow)] = 'Monthly Expenses'
wsB['E' + str(wsBrow)] = 'monthly Income'
wsBHrow = wsBrow
wsBrowExp = wsBrow + 1
wsBrowInc = wsBrow + 1
#create the budget rows
for e in expenses:
    wsB['A' + str(wsBrowExp)] = e
    wsBrowExp = wsBrowExp + 1
for i in income:
    wsB['E' + str(wsBrowInc)] = i
    wsBrowInc = wsBrowInc + 1
#create the budget totals
wsB['A' + str(wsBrowExp)] = 'TotalExpenses'
wsB['B' + str(wsBrowExp)] = '=SUM(B' + str(wsBHrow + 1) + ':B' + str(wsBrowExp - 1) +')'
BExpTotal = 'B' + str(wsBrowExp)
wsB['E' + str(wsBrowInc)] = 'TotalIncome'
wsB['F' + str(wsBrowInc)] = '=SUM(F' + str(wsBHrow + 1) + ':F' + str(wsBrowInc - 1) +')'
BIncTotal = 'F' + str(wsBrowInc)

#create column headers


#create the month.
def create_month(ws):
    wsMrowInc = wsMrow
    wsMrowAna = wsMrow
    column = 'A'
    IncTotal ={}

    #income column
    # header
    ws[column + str(wsMrowInc)] = 'Income'
    ws[column + str(wsMrowInc)].font = Font(bold=True)
    print(column + str(wsMrowAna) + ':' + chr(ord(column)+2) + str(wsMrowAna))
    ws.merge_cells(column + str(wsMrowAna) + ':' + chr(ord(column)+2) + str(wsMrowAna))
    wsMrowInc = wsMrowInc + 1
    #income section
    for i in incomeCats:
      ws[column + str(wsMrowInc)] = i['name'] + ' Income'
      ws[column + str(wsMrowInc)].font = Font(bold=True)
      wsMHrowInc = wsMrowInc
      wsMrowInc = wsMrowInc + 1
      ##income catagories
      for j in subcat[i['name']]:
        ws[chr(ord(column)+1) + str(wsMrowInc)] = j['name']
        wsMrowInc = wsMrowInc + 1
      ##income total
      ws[chr(ord(column)+1) + str(wsMrowInc)] = i['name'] + ' Total'
      ws[chr(ord(column)+1) + str(wsMrowInc)].font = Font(bold=True)
      ws[chr(ord(column)+2) + str(wsMrowInc)] = '=SUM(' + chr(ord(column)+2) + str(wsMHrowInc + 1) + ':' + chr(ord(column)+2) + str(wsMrowInc - 1) +')'
      ws[chr(ord(column)+2) + str(wsMrowInc)].font = Font(bold=True)
      IncTotal[i['name']] = chr(ord(column)+2) + str(wsMrowInc)
      print(IncTotal[i['name']])
      wsMrowInc = wsMrowInc + 1
      
    ##Total Income
    ws[column + str(wsMrowInc)] = 'Total Income'
    ws[column + str(wsMrowInc)].font = Font(bold=True)
    ws[chr(ord(column)+2) + str(wsMrowInc)] = '=SUM(' + earnedIncTotal + '+' + passiveIncTotal + '+' + portfolioIncTotal +')'
    ws[chr(ord(column)+2) + str(wsMrowInc)].font = Font(bold=True)
    IncTotal = chr(ord(column)+2) + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 2

    #Expenses column
    # header
    ws['A' + str(wsMrowInc)] = 'Expenses'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    wsMrowInc = wsMrowInc + 1
    #Household Expenses section
    ws['A' + str(wsMrowInc)] = 'Household Expenses'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    wsMHrowInc = wsMrowInc
    wsMrowInc = wsMrowInc + 1
    ##Household Expenses catagories
    for he in houseExpenses:
      ws['B' + str(wsMrowInc)] = he
      wsMrowInc = wsMrowInc + 1
    ##Household Expenses total
    ws['B' + str(wsMrowInc)] = 'Household Total'
    ws['B' + str(wsMrowInc)].font = Font(bold=True)
    ws['C' + str(wsMrowInc)] = '=SUM(C' + str(wsMHrowInc + 1) + ':C' + str(wsMrowInc - 1) +')'
    ws['C' + str(wsMrowInc)].font = Font(bold=True)
    householdExpTotal = 'C' + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 1
    #DJ Expenses section
    ws['A' + str(wsMrowInc)] = 'DJ Expenses'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    wsMHrowInc = wsMrowInc
    wsMrowInc = wsMrowInc + 1
    ##DJ Expenses catagories
    for de in djExpenses:
      ws['B' + str(wsMrowInc)] = he
      wsMrowInc = wsMrowInc + 1
    ##DJ Expenses total
    ws['B' + str(wsMrowInc)] = 'DJ Total'
    ws['B' + str(wsMrowInc)].font = Font(bold=True)
    ws['C' + str(wsMrowInc)] = '=SUM(C' + str(wsMHrowInc + 1) + ':C' + str(wsMrowInc - 1) +')'
    ws['C' + str(wsMrowInc)].font = Font(bold=True)
    djExpTotal = 'C' + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 1
    #Personal Expenses section
    ws['A' + str(wsMrowInc)] = 'Personal Expenses'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    wsMHrowInc = wsMrowInc
    wsMrowInc = wsMrowInc + 1
    ##Personal Expenses catagories
    for pe in personalExpenses:
      ws['B' + str(wsMrowInc)] = pe
      wsMrowInc = wsMrowInc + 1
    ##Personal Expenses total
    ws['B' + str(wsMrowInc)] = 'Personal Total'
    ws['B' + str(wsMrowInc)].font = Font(bold=True)
    ws['C' + str(wsMrowInc)] = '=SUM(C' + str(wsMHrowInc + 1) + ':C' + str(wsMrowInc - 1) +')'
    ws['C' + str(wsMrowInc)].font = Font(bold=True)
    personalExpTotal = 'C' + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 1
    ##Total Expenses
    ws['A' + str(wsMrowInc)] = 'Total Expenses'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    ws['C' + str(wsMrowInc)] = '=SUM(' + householdExpTotal + '+' + djExpTotal + '+' + personalExpTotal +')'
    ws['C' + str(wsMrowInc)].font = Font(bold=True)
    ExpTotal = 'C' + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 2

    #Net monthly Cash flow
    ws['A' + str(wsMrowInc)] = 'Net Monthly Cash Flow'
    ws['A' + str(wsMrowInc)].font = Font(bold=True)
    ws['C' + str(wsMrowInc)] = '=SUM(' + IncTotal + '-' + ExpTotal + ')'
    ws['C' + str(wsMrowInc)].font = Font(bold=True)
    NetTotal = 'C' + str(wsMrowInc)
    wsMrowInc = wsMrowInc + 2
    
    #analysis column
    ws['E' + str(wsMrowAna)] = 'Analysis'
    ws['E' + str(wsMrowAna)].font = Font(bold=True)
    ws.merge_cells('E' + str(wsMrowAna) + ':' + 'G' + str(wsMrowAna))
    wsMrowAna = wsMrowAna + 1
    #Cash Flow
    ws['E' + str(wsMrowAna)] = 'How much do you keep?'
    wsMrowAna = wsMrowAna + 1
    ws['E' + str(wsMrowAna)] = 'Cash Flow/Total Income'
    ws['F' + str(wsMrowAna)] = '=SUM(' + NetTotal + '/' + IncTotal + ')'
    ws['F' + str(wsMrowAna)].style = 'Percent'
    wsMrowAna = wsMrowAna + 1
    ws['E' + str(wsMrowAna)] = '***should be increasing'
    ws['E' + str(wsMrowAna)].font = Font(size=8)
    return(ws)

wsJan = create_month(wsJan)
wsFeb = create_month(wsFeb)
wsMar = create_month(wsMar)
wsMay = create_month(wsMay)
wsApr = create_month(wsApr)
wsJun = create_month(wsJun)
wsJul = create_month(wsJul)
wsAug = create_month(wsAug)
wsSep = create_month(wsSep)
wsOct = create_month(wsOct)
wsNov = create_month(wsNov)
wsDec = create_month(wsDec)

# Create the Overview table heading row
wsO['A' + str(wsOrow)] = 'Month'
wsO['B' + str(wsOrow)] = 'Actual Expenses'
wsO['C' + str(wsOrow)] = 'Budget expenses'
wsO['D' + str(wsOrow)] = '+/-'
wsO['E' + str(wsOrow)] = 'Actual Income'
wsO['F' + str(wsOrow)] = 'Budget Income'
wsO['G' + str(wsOrow)] = '+/-'
wsO['H' + str(wsOrow)] = 'Actual Balance'
wsO['I' + str(wsOrow)] = 'Budget Balance'
wsO['J' + str(wsOrow)] = '+/-'
wsOHrow = wsOrow
wsOrow = wsOrow + 1

#Create the rows in the overview table
for m in months:
    wsO['A' + str(wsOrow)] = m
    wsO['B' + str(wsOrow)] = '=' + m +'!C68'
    wsO['C' + str(wsOrow)] = '=Budget!' + str(BExpTotal)
    wsO['D' + str(wsOrow)] = '=SUM(B' + str(wsOrow) + '-C' + str(wsOrow) + ')'
    wsO['E' + str(wsOrow)] = '=' + m +'!C22'
    wsO['F' + str(wsOrow)] = '=Budget!' + str(BIncTotal)
    wsO['G' + str(wsOrow)] = '=SUM(E' + str(wsOrow) + '-F' + str(wsOrow) + ')'
    wsO['H' + str(wsOrow)] = '=SUM(E' + str(wsOrow) + '-B' + str(wsOrow) + ')'
    wsO['I' + str(wsOrow)] = '=SUM(F' + str(wsOrow) + '-C' + str(wsOrow) + ')'
    wsO['J' + str(wsOrow)] = '=SUM(H' + str(wsOrow) + '-I' + str(wsOrow) + ')'
    wsOrow = wsOrow + 1

#create the totals row in the overview table
wsO['A' + str(wsOrow)] = 'Totals'
wsO['B' + str(wsOrow)] = '=SUM(B' + str(wsOHrow + 1) + ':B' + str(wsOrow - 1) +')'
wsO['C' + str(wsOrow)] = '=SUM(C' + str(wsOHrow + 1) + ':C' + str(wsOrow - 1) +')'
wsO['D' + str(wsOrow)] = '=SUM(D' + str(wsOHrow + 1) + ':D' + str(wsOrow - 1) +')'
wsO['E' + str(wsOrow)] = '=SUM(E' + str(wsOHrow + 1) + ':E' + str(wsOrow - 1) +')'
wsO['F' + str(wsOrow)] = '=SUM(F' + str(wsOHrow + 1) + ':F' + str(wsOrow - 1) +')'
wsO['G' + str(wsOrow)] = '=SUM(G' + str(wsOHrow + 1) + ':G' + str(wsOrow - 1) +')'
wsO['H' + str(wsOrow)] = '=SUM(H' + str(wsOHrow + 1) + ':H' + str(wsOrow - 1) +')'
wsO['I' + str(wsOrow)] = '=SUM(I' + str(wsOHrow + 1) + ':I' + str(wsOrow - 1) +')'
wsO['J' + str(wsOrow)] = '=SUM(J' + str(wsOHrow + 1) + ':J' + str(wsOrow - 1) +')'

# Save the file
wb.save("Financal Statement.xlsx")
