import os
from google.cloud import bigquery
from google.oauth2 import service_account
from configs.logger import get_logger


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

        query = """
                SELECT 
                *
                FROM 
                    `bigquery-public-data.hacker_news.full`
                WHERE
                    score IS NOT NULL
                    AND text IS NOT NULL
                    AND EXTRACT(YEAR FROM timestamp) = @year
                ORDER BY
                    score DESC
                LIMIT 1000;
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("year", "INT64", 2022),
            ]
        )

        query_job = client.query(query, job_config=job_config)
        df = query_job.to_dataframe()
        logger.info(f'Query returned {len(df)} rows and {len(df.columns)} columns')
        return df
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        exit(1)