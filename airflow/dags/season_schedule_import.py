from airflow.models import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd 

from app.service.etl.bball_reference.bball_reference_client import BballReferenceClient
from app.service.storage.storage_provider import StorageProvider

dag = DAG(
    dag_id="season_schedule_import",
    schedule_interval="0 0 10 10 *",
    start_date='2010-01-01',
    catchup=True
)

def _download_season_to_raw_file(**kwargs):
    logical_date = kwargs['logical_date']
    logical_year = logical_date.year + 1

    client = BballReferenceClient()
    raw_schedule_data = client.get_schedule_raw(logical_year)

    assert isinstance(raw_schedule_data, pd.DataFrame)

    print("RAW SCHEDULE")
    print(raw_schedule_data)

    file_name = f"{logical_year}.json"
    storage_provider = StorageProvider()
    storage_provider.upload_file(
        "etl", 
        f"season/schedule/{file_name}",
        raw_schedule_data.to_json(file_name, indent=4)
    )

download_season_to_raw_file = PythonOperator(
    task_id="download_season_to_raw_file", 
    python_callable=_download_season_to_raw_file, 
    dag=dag
)

download_season_to_raw_file >> exit


if __name__ == "__main__":
    dag.test()