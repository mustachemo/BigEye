from dotenv import load_dotenv
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from configs.logger import get_logger

logger = get_logger(__name__)


def load_data_to_bigquery(df):
    load_dotenv()

    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)

        dataset_ref = client.dataset("gdeltv2", project="gdelt-bq")
        table_ref = dataset_ref.table("usa_events")
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("GLOBALEVENTID", "INT64"),
                bigquery.SchemaField("SQLDATE", "DATE"),
                bigquery.SchemaField("MonthYear", "DATE"),
                bigquery.SchemaField("Actor1Name", "STRING"),
                bigquery.SchemaField("Actor2Name", "STRING"),
                bigquery.SchemaField("EventCode", "STRING"),
                bigquery.SchemaField("SourceURL", "STRING"),
            ],
            write_disposition="WRITE_TRUNCATE",
        )

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Waits for the job to complete

        table = client.get_table(table_ref)
        logger.info(f'Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_ref.path}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')