import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port') 
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')

def main(pg_user, pg_pass, pg_host, pg_port, pg_db):


    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Green taxi dataset
    df = pd.read_parquet("green_tripdata_2025-11.parquet")
    # Taxi zone lookup dataset
    df_zone = pd.read_csv("taxi_zone_lookup.csv")

    # Print the schema from df
    print(pd.io.sql.get_schema(df, name='green_taxi_data_nov_25', con=engine))

    # Create the table in postgres
    df.head(n=0).to_sql(name='green_taxi_data_nov_25', con=engine, if_exists='replace')

    # Ingest data to database
    # df.to_sql(name='green_taxi_data_nov_25', con=engine, if_exists='append')
    # df_zone.to_sql(name='taxi_zone', con=engine, if_exists='append')


if __name__ == "__main__":
    main()
