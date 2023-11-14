import streamlit as st
from google.cloud import bigquery
import os
from tools import fetch_data, sort, plot_graph, integrate_changes, write_data, run_dbt
dir_path = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

DBT_EXEC_PATH = os.environ['DBT_EXEC_PATH']
DBT_PROJ_DIR = os.environ['DBT_PROJ_DIR']
BIGQUERY_PROJECT = os.environ['BIGQUERY_PROJECT']

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


#---------------------------Streamlit App ----------------------#

## Title
st.title("Load - Capacity App")

# Instruction
st.markdown('Welcome to your Load Capacity Simulation scenario powered by BigQuery and DBT')


#--------------------------- Configure the Sidebar ----------------------#

st.sidebar.image("iris_logo.png")

with st.sidebar:
    st.header('Filters')
    # Dynamic scenario selection in the sidebar
    selected_scenarios = st.multiselect('Select Scenarios', options=[1, 2, 3], default=1, key='scenario_select')
    selected_lines = st.multiselect('Select Lines', options=["Line_1", "Line_2", "Line_3", "Line_4", "Line_5"], key='line_select')



# Plot the graph of load-capacity
load_capacity_data = fetch_data('load_capacity', 'gabriel', BIGQUERY_PROJECT)
sorted_data = sort(load_capacity_data, "day")
st.session_state['load_capacity_data'] = sorted_data
fig = plot_graph(st.session_state['load_capacity_data'], selected_scenarios, selected_lines)
# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True)


# Display the capacity parameters table

if 'data' not in st.session_state:
    df = fetch_data('capacity_parameters', 'gabriel', BIGQUERY_PROJECT)
    df['id'] = df.index
    st.session_state['data'] = sort(df, "Day_of_the_Week")
    st.session_state['full_data'] = st.session_state['data'].copy()

    
filtered_data = st.session_state['data'][(st.session_state['data']['Sc'].isin(selected_scenarios))]
edited_data = st.data_editor(filtered_data, num_rows="dynamic", disabled=("Day_of_the_Week"), column_config={"id": None}, hide_index=True, width= 2000)
st.session_state['edited_data'] = edited_data  # Store edited data in session state


# Button to submit changes and run dbt
if st.button('Submit Changes'):
    updated_full_data = integrate_changes(st.session_state['full_data'], st.session_state['edited_data'], 'id')
    write_data(updated_full_data, 'gabriel.capacity_parameters', BIGQUERY_PROJECT)
    stdout, stderr = run_dbt(DBT_EXEC_PATH, DBT_PROJ_DIR)
    if stderr:
        st.error(f"DBT Run Error: {stderr.decode('utf-8', errors='replace')}")
    else:
        st.runtime.legacy_caching.clear_cache()
        # Fetch the updated load_capacity data
        load_capacity_data = fetch_data('load_capacity', 'gabriel', BIGQUERY_PROJECT)
        sorted_data = sort(load_capacity_data, "day")
        st.session_state['load_capacity_data'] = sorted_data
        st.rerun()



