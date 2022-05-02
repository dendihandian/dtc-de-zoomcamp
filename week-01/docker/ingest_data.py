from time import time
from sqlalchemy import create_engine
import os
import argparse
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)

def main(params):

    logging.debug('extracting parameters into respective variables')
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url


    logging.debug('downloading the csv and rename it into output.csv')
    csv_name = 'output.csv'
    os.system(f"wget {url} -O {csv_name}")

    logging.debug('creating postgres engine')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # load the csv data into pandas dataframe
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    # convert the designated columns to datetime types
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # create table, if exists replace it
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # dump the dataframe into postgres table
    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

# the __main__ function (to execute)
if __name__ == '__main__':
    # initiate a parser
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # get the parameters/arguments executed from the CLI command
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    # wrap arguments into dictionary variable
    args = parser.parse_args()

    # execute the main function
    main(args)