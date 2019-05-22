import sqlite3 as lite 
import sys

con = None

query_string = '''
SELECT City
FROM Customer, Invoice
WHERE Customer.CustomerId = Invoice.CustomerId
GROUP BY City
ORDER BY sum(Total) DESC
LIMIT 3
'''

try:
  con = lite.connect('Chinook_Sqlite.sqlite')
  cur = con.cursor()  
  cur.execute(query_string)  

  print(cur.fetchall())
except Exception as e:
  print(e)
  sys.exit(1)
finally:
  if con is not None:
    con.close()
