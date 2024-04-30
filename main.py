from etl.extract import extract_data_from_bigquery
from etl.load import load_data_to_bigquery
import pandas as pd


if __name__ == '__main__':
    df = extract_data_from_bigquery()
    df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')
    df['MonthYear'] = pd.to_datetime(df['MonthYear'], format='%Y%m')
    load_data_to_bigquery(df)