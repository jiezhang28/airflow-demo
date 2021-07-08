import json
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

dag = DAG(
    dag_id='process_numbers',
    schedule_interval=None,
    default_args={
        'owner': 'jie',
        'start_date': datetime(2021,7,1),
    }
)

file_sensor = FileSensor(
    task_id='file_sensor',
    dag=dag,
    file_path='/data/numbers.json',
    poke_interval=5,
)

stage_file = BashOperator(
    task_id='stage_file',
    dag=dag,
    bash_command="""
        STAGE_FILE=/data/stage/numbers_$(date +%s).json
        mkdir -p /data/stage
        mv /data/numbers.json ${STAGE_FILE}
        echo $STAGE_FILE
    """,
)

def write_sum_func(file_name):
    with open(file_name, 'r') as f:
        numbers = json.load(f)

    total = sum(numbers)
    with open('/data/output.csv', 'a') as f:
        f.write(f'{file_name},{total}\n')

write_sum = PythonOperator(
    task_id='write_sum',
    dag=dag,
    python_callable=write_sum_func,
    op_args=["{{ task_instance.xcom_pull(task_ids='stage_file') }}"],
)

file_sensor >> stage_file >> write_sum

