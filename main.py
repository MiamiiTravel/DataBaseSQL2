import sqlite3 as lite 
import sys

con = None

query_string1 = '''
SELECT C.FirstName, C.LastName, C.Phone, C.City FROM Customer C JOIN (
    SELECT C1.City, C1.CustomerId FROM Customer C1
    inner join Invoice 
    on C1.CustomerId = Invoice.CustomerId
    group by C1.City 
    having count(distinct C1.CustomerId) > 1
) TMP1 ON TMP1.City = C.City 
INNER JOIN Invoice X ON C.CustomerId =X.CustomerId 
GROUP BY C.CustomerId;
'''

query_string2 = '''
SELECT City
FROM Customer, Invoice
WHERE Customer.CustomerId = Invoice.CustomerId
GROUP BY City
ORDER BY sum(Total) DESC
LIMIT 3
'''
query_string3 = '''
SELECT T1.Name Genre, Track.Name Track, Album.Title, Artist.Name Artist
FROM Track, Album, Artist, (SELECT Genre.GenreId, Genre.Name
                            FROM Track
                            INNER JOIN Genre ON Genre.GenreId = Track.GenreId
                            INNER JOIN InvoiceLine ON Track.TrackId = InvoiceLine.TrackId
                            GROUP BY Track.GenreId
                            ORDER BY count(Track.GenreId) DESC
                            LIMIT 1
                           ) T1
WHERE Track.AlbumId = Album.AlbumId
AND Album.ArtistId = Artist.ArtistId
AND Track.GenreId = T1.GenreId
ORDER BY Artist.Name
'''

def data(query_string):
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
  return data 
      
