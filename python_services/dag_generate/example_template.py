import datetime
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import requests
import pathlib

# define city as a Jinja placeholder
city = "{{ city }}"
dag_id = f"auto_generated_{city}_weather_update"

report_location = pathlib.Path(__file__).parent.parent / "weather_updates"
if not report_location.exists():
    report_location.mkdir()


@task
def generate_report(city):
    response = requests.get(f"http://wttr.in/{city}")
    if response.ok:
        return response.text
    return None

{% if is_european %}
# if the city is European, define the write_report function
@task
def write_report(city, report_data):
    report_file = report_location / f"{city}.txt"
    print(f"writing data to {report_file}...")
    with open(report_file, "w") as f:
        f.write(report_data)
{% else %}
# if the city is not European, define the print_report function
@task
def print_report(city, report_data):
    print(f"This is the weather report for: {city}")
    print(report_data)
{% endif %}

@dag(
    dag_id=f"auto_generated_{city}_weather_update",
    start_date=datetime.datetime(2022, 1, 1),
    schedule_interval=None)
def my_dag():
    report_data = generate_report(city)
    {% if is_european %}
    # if the city is European, call write_report
    write_report(city, report_data)
    {% else %}
    # if the city is not European, call print_report
    print_report(city, report_data)
    {% endif %}

dag = my_dag()