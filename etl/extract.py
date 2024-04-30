import os
from google.cloud import bigquery
from google.oauth2 import service_account
from configs.logger import get_logger

# Set up logging
logger = get_logger(__name__)

# Check if environment variable is set
if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    logger.error('GOOGLE_APPLICATION_CREDENTIALS environment variable is not set')
    exit(1)

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def extract_data_from_bigquery():
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)

        dataset_ref = client.dataset("gdeltv2", project="gdelt-bq")
        dataset = client.get_dataset(dataset_ref)
        tables = list(client.list_tables(dataset))
        logger.info(f'Dataset {dataset.dataset_id} contains {len(tables)} tables')

        query = """
        SELECT GLOBALEVENTID, SQLDATE, MonthYear, Actor1Name, Actor2Name, EventCode, SourceURL
        FROM `gdelt-bq.gdeltv2.events`
        WHERE Year = @year AND Actor1CountryCode = 'USA'
        AND (Actor1Geo_CountryCode = 'US' AND Actor1Geo_ADM1Code LIKE 'US%')
        LIMIT 10;
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("year", "INT64", 2021)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        df = query_job.to_dataframe()
        print(df)
        logger.info(f'Query returned {len(df)} rows')
        return df
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        exit(1)