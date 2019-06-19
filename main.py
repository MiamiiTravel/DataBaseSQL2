import sqlite3 as lite
import sys
import pprint


query_string_first_task = '''
SELECT C.FirstName, C.LastName, C.Phone, C.City FROM Customer C JOIN (
    SELECT C1.City, C1.CustomerId FROM Customer C1
    inner join Invoice 
    on C1.CustomerId = Invoice.CustomerId
    group by C1.City 
    having count(distinct C1.CustomerId) > 1
) TMP1 ON TMP1.City = C.City 
inner join Invoice X on C.CustomerId =X.CustomerId 
group by C.CustomerId;
'''
query_string_second_task = '''
select c.City, round(sum(i.Total),2) as t from Customer c inner join Invoice I on c.CustomerId = I.CustomerId
group by c.City
order by t DESC
limit 3;
'''
query_string_third_task = '''
select t.name as GenreName,
       T1.name as Track,
       A.title as Album,
       A2.Name as Artist
FROM (select G.GenreId, G.name
    from InvoiceLine IL
    JOIN Track T ON T.trackId = IL.trackId
    Join Genre G ON G.GenreId = T.GenreId
    group by G.GenreId
    order by sum(quantity) DESC limit 1) t
Join Track T1 ON T1.GenreId  = t.GenreId
LEFT JOIN Album A ON A.AlbumId = T1.AlbumId
LEFT JOIN Artist A2 ON A2.ArtistId = A.artistId
;
'''


def db_output(query_string):
    try:
        con = lite.connect('Chinook_Sqlite.sqlite')
        cur = con.cursor()
        cur.execute(query_string)

        data = cur.fetchall()
        pprint.pprint(data)
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()
    return data
db_output(query_string_first_task)
db_output(query_string_second_task)
db_output(query_string_third_task)
