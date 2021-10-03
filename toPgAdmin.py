import os
from Tools.scripts.fixcid import err
from psycopg2 import OperationalError, errorcodes, errors
import pandas as pd
import psycopg2
import sys


def show_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occurred
    line_n = traceback.tb_lineno
    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def connect_db(conn_params_dic):
    try:
        print('Connecting to the PostgreSQL...........')
        conn = psycopg2.connect(**conn_params_dic)
        print("Connected successfully..................")
    except OperationalError as err:
        # passing exception to function
        show_psycopg2_exception(err)
        # set the connection to 'None' in case of error
        conn = None
    return conn


def copy_from_dataFile(conn, df, table):
    tmp_df = "symbols_data.csv"
    df.to_csv(tmp_df, header=False, index=False)
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        print("In try")
        print("table:", table)
        cursor.copy_from(f, table, sep="\t")
        conn.commit()
        print("Data inserted using copy_from_datafile() successfully....")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("In except")
        # f.close()
        os.remove(tmp_df)
        # pass exception to function
        cursor.close()
    print("copy_from_file() done")
    cursor.close()
    #f.close()
    os.remove(tmp_df)


if __name__ == '__main__':
    df = pd.read_json('symbols_data.json')
    df.info()
    conn_params_dic = {
        "host": "database-1-instance-1.cjnqt4tn6fbq.us-east-1.rds.amazonaws.com",
        "database": "postgres",
        "user": "postgres",
        "password": "rico2021"
    }
    conn = connect_db(conn_params_dic)
    print("conn:", conn)
    copy_from_dataFile(conn, df, 'stock.symbols')
    conn.close()
