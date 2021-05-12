from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    dag_id='hello_world',
    schedule_interval='0 0 * * *',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2021, 5, 1),
    },
)

task = BashOperator(
    task_id='print_hello_world',
    dag=dag,
    bash_command='echo "Hello World!',
)

