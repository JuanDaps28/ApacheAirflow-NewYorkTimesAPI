# ApacheAirflow-NewYorkTimesAPI
 This repository integrates a free New York Times rest API with an airflow data pipeline. The project is built with docker compose to set all the needed instances, services and databases.

 The data pipeline consists in a basic ETL process, built with python, that extracts the metadata about the most emailed articles from the New York Times, cleans the data and loads the information inside a postgresql database. Everything runs inside multiple docker containers which are set and configured in the docker-compose.yaml file.

# New York Times API
You can get more information about the api in the documentation:
https://developer.nytimes.com/docs/most-popular-product/1/overview

Also to know how to get the api key you can read the followong documentation:
https://developer.nytimes.com/get-started

# First steps
Before start running the docker compose file, it's necessary to create a .env file to set some environment variables inside the containers. In the .env file create the following variables:

AIRFLOW_IMAGE_NAME=apache/airflow:2.3.0
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=??????????
_AIRFLOW_WWW_USER_PASSWORD=??????????
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
API_KEY=??????????

In the case of API_KEY variable, it's necessary to follow the steps explained in the New York Times api documentation (https://developer.nytimes.com/get-started) to create an api key that allows get the api data. Once you have the api key created, you can put its value in this variable.

The variables _AIRFLOW_WWW_USER_USERNAME and _AIRFLOW_WWW_USER_PASSWORD are the corresponding credentials to login airflow as admin. You can set a username and password in this variables or, if you want, you can delete these variables and airflow will take "airflow" as username and password by default.

# Run docker-compose
With all the previous steps succesfully completed, you can now start the docker containers. For that open a terminal in the folder where the docker-compose.yaml is located and run the following:

docker-compose up -d

In general, this command will take the configuration set in the docker-compose.yaml file and will start running the containers, which includes a redis and postgresql databases, the whole services for airflow (web server, scheduler, celery worker), the volumes required and the environment variables set in the .env file.

In the following documentation you can find more information about running airflow with docker:
https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html

# Airflow
Once the whole containers are up, you can access localhost:8080 (defined port to connect ariflow services) and you will have the airflow maine page, where you can login and see the nyt_dag created. Now you can get inside the dag and run it to test it.

In the repository, inside the dags folder, you can find the python file where the dag is configured, feel free to modify the code as needed.

The following documentation gives more information about dags in airflow:
https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html

You can get in postgresl container and run a query to validate data in tables with the following commands

docker-compose ps 
docker exec -it {postgresql docker name} /bin/bash
psql -U airflow
SELECT * FROM nyt_articles;

# Finish docker containers
To finish the docker containers you can run:

docker-compose down

Or if you want to remove the whole data about the containers and volumes:

docker-compose down --volumes --rmi all