import json

import pandas as pd
import pymysql
from sqlalchemy import create_engine

# df = pd.read_json('symbols_data.json')
# df.info()
engine = create_engine('postgresql+psycopg2://postgres:rico2021@database-1-instance-1.cjnqt4tn6fbq.us-east-1.rds'
                       '.amazonaws.com/postgres')
file = 'symbols_data.json'
with open(file) as train_file:
    dict_train = json.load(train_file)
# print(dict_train)
train = pd.DataFrame.from_dict(dict_train, orient='index')
print(train)
train.reset_index(level=0, inplace=True)
print(train)
train.to_sql('symbols', con=engine, schema='stock', if_exists='replace')
