import os
import psycopg2
import requests
import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from airflow.decorators import dag, task

number_periods = 1
API_endpoint = f"https://api.nytimes.com/svc/mostpopular/v2/emailed/{number_periods}.json?api-key={os.environ['API_KEY']}"

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False
}

@dag(default_args = default_args, start_date = datetime(2022, 9, 4), schedule_interval='@daily')
def nyt_dag():

    @task
    def extract_most_emailed_articles():
        return requests.get(API_endpoint).json()['results']

    @task
    def transform_most_emailed_articles(data):
        data = pd.json_normalize(data)
        data = data[['uri', 'url', 'id', 'source', 'published_date', 'updated', 'section', 'subsection', 'nytdsection', 'adx_keywords', 'byline', 'type', 'title', 'abstract']]
        data = data.to_dict('records')
        return data

    @task
    def create_nyt_articles_table():
        conn = psycopg2.connect(dbname=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host='postgres')
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS nyt_articles (
                uri varchar(500),
                url varchar(500),
                id varchar(500),
                source varchar(500),
                published_date varchar(500),
                updated varchar(500),
                section varchar(500),
                subsection varchar(500),
                nytdsection varchar(500),
                adx_keywords varchar(500),
                byline varchar(500),
                type varchar(500),
                title varchar(500),
                abstract varchar(500)
            );"""
        )
        conn.commit()
        conn.close()
        cur.close()

    @task
    def load_most_emailed_articles(data):
        conn = psycopg2.connect(dbname=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host='postgres')
        cur = conn.cursor()
        for record in data:
            column_list = ', '.join(record.keys())
            values_list = ', '.join(["'"+str(x).replace("'", "")+"'" for x in record.values()])
            query = f"INSERT INTO nyt_articles ({column_list}) VALUES ({values_list})"
            cur.execute(query)
        conn.commit()
        conn.close()
        cur.close()

    create_nyt_articles_table() >> load_most_emailed_articles(transform_most_emailed_articles(extract_most_emailed_articles()))

dag = nyt_dag()