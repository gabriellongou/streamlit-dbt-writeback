import streamlit as st
import pandas as pd
from pandas_gbq import to_gbq
from google.cloud import bigquery
import subprocess
import os
import plotly.graph_objs as go
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import bigquery

load_dotenv()
dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

DBT_EXEC_PATH = os.environ['DBT_EXEC_PATH']
DBT_PROJ_DIR = os.environ['DBT_PROJ_DIR']
BIGQUERY_PROJECT = os.environ['BIGQUERY_PROJECT']

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)



# Sort days of the week
def sort(df, field):
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df[field] = pd.Categorical(df[field], categories=days_order, ordered=True)
    return df.sort_values(field)

def fetch_data(table, dataset, project):
    query = f"""
        SELECT * FROM `{project}.{dataset}.{table}`
    """
    data = client.query(query).to_dataframe()
    return data

def write_data(dataframe, table_id, project_id):
    to_gbq(dataframe, table_id, project_id = project_id, if_exists='replace', credentials=credentials)

import plotly.graph_objs as go
import plotly.express as px

def plot_graph(data, selected_scenarios, selected_lines):
    if selected_lines:
        data = data[data['line'].isin(selected_lines)]
    bar_data = data.groupby('day').load_all_factories.sum().reset_index()
    bar_data['load_all_factories'] /= 3
    bar_chart = go.Bar(x=bar_data['day'], y=bar_data['load_all_factories'], name='Load', marker_color='#87737B')

    # Initialize list to store line chart traces
    line_charts = []

    # Define a set of colors for different lines
    colors = ['#901237', '#123456', '#654321']  # You might want to extend this list for more scenarios

    # Plotting the line chart for each selected scenario
    for i, scenario in enumerate(selected_scenarios):
        scenario_line_data = data[data['scenario'] == scenario]
        line_data = scenario_line_data.groupby('day').capacity.sum().reset_index()
        line_chart = go.Scatter(x=line_data['day'], y=line_data['capacity'], mode='lines+markers', name=f'Capacity (Scenario {scenario})', line=dict(color=colors[i % len(colors)]))
        line_charts.append(line_chart)

    # Combine bar and line plots
    fig = go.Figure(data=[bar_chart] + line_charts)

    # Update layout
    fig.update_layout(
        title='Load vs Capacity by Day',
        xaxis_title='Day of the Week',
        yaxis_title='Load / Capacity',
        bargap=0.3
    )

    return fig


def run_dbt(dbt_executable_path, dbt_project_directory):
    command = "dbt run --select stg_capacity_parameters+"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dbt_project_directory)
    stdout, stderr = process.communicate()
    return stdout, stderr

def integrate_changes(full_data, edited_data, unique_id_col):
    for edited_id in edited_data[unique_id_col]:
        # Find the corresponding row in full_data
        matching_index = full_data[full_data[unique_id_col] == edited_id].index

        # If a matching index is found, update the corresponding row in full_data
        if not matching_index.empty:
            # Ensure that the edited row has the same columns as the full_data
            edited_row = edited_data[edited_data[unique_id_col] == edited_id].iloc[0]
            for col in full_data.columns:
                if col in edited_row:
                    full_data.at[matching_index[0], col] = edited_row[col]

    return full_data




