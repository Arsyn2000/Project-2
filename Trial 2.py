# sample of code that worked for me

import psycopg2  # import the postgres library

# connect to the database
conn = psycopg2.connect(host='database-1-instance-1.cjnqt4tn6fbq.us-east-1.rds.amazonaws.com',
                        dbname='postgres',
                        user='postgres',
                        password='rico2021',
                        port='5432')
# create a cursor object
# cursor object is used to interact with the database
cur = conn.cursor()

# open the csv file using python standard file I/O
# copy file into the table just created
with open('symbols_data.csv', 'r') as f:
    next(f)  # Skip the header row.
    # f , <database name>, Comma-Seperated
    cur.copy_from(f, 'Rico.postgres.stock.symbols', sep=',')
    # Commit Changes
    conn.commit()
    # Close connection
    conn.close()

f.close()
