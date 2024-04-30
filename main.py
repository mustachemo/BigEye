from etl.extract import extract_data_from_bigquery


if __name__ == '__main__':
    df = extract_data_from_bigquery()

    print(df.head())
    