import pandas as pd
from datetime import datetime

def transform(df):
    df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d')
    df['MonthYear'] = pd.to_datetime(df['MonthYear'], format='%Y%m')
    return df

df = transform(df)
