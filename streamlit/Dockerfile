# app/Dockerfile
FROM python:3.11.5-slim

# Expose port you want your app on
EXPOSE 8080

# IMPORTANT : for Streamlit version 1.10.0 and higher, Streamlit apps cannot be run from the root directory of Linux distributions.
WORKDIR /app

ENV DBT_EXEC_PATH "/usr/local/bin/dbt"
ENV DBT_PROJ_DIR "/app/dbt_bigquery"
ENV BIGQUERY_PROJECT "molten-plate-403016"
ENV DBT_PROFILES_DIR "/app/dbt_bigquery/.dbt"

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
# COPY text_explorer text_explorer 
COPY main.py main.py
COPY tools.py tools.py
COPY dbt_bigquery dbt_bigquery
COPY .streamlit .streamlit
COPY iris_logo.png iris_logo.png
COPY key.json key.json

# Run
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]