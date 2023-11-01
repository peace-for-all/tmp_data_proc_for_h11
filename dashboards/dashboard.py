import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import os
import sys

# Append the path to db/connector.py to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # todo hacky, get rid
from db.connector import Connector


# todo fix select all, make it more flexible
def select_all(table_name):
    con = Connector()
    engine = con.get_engine()

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)

    return df


# Process data
def process_data(df):
    # Melt the DataFrame to have Skills in a single column
    skills_df = pd.melt(df, id_vars=['DateTime', 'JobTitle', 'Company'], value_vars=[f'Skill{i}' for i in range(1, 11)],
                        value_name='Skill')
    skills_df = skills_df.dropna().drop('variable', axis=1)
    return skills_df


# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Graph(id='graph-skills'),
    dcc.Dropdown(
        id='dropdown-job-title',
        options=[],
        multi=True,
        value=[],
        placeholder="Select Job Titles"
    ),
    dcc.Graph(id='graph-skills-per-day')
])


# Callback to populate dropdown
@app.callback(
    Output('dropdown-job-title', 'options'),
    Input('dropdown-job-title', 'search_value')
)
def set_job_title_options(search_value):
    df = select_all('skills_daily')
    job_titles = df['JobTitle'].unique()
    return [{'label': jt, 'value': jt} for jt in job_titles]


# Callback to update graph
@app.callback(
    Output('graph-skills', 'figure'),
    Output('graph-skills-per-day', 'figure'),
    Input('dropdown-job-title', 'value')
)
def update_graph(selected_job_titles):
    df = select_all('skills_daily')
    skills_df = process_data(df)

    if selected_job_titles:
        skills_df = skills_df[skills_df['JobTitle'].isin(selected_job_titles)]

    # Skill distribution graph
    fig_skills = px.histogram(skills_df, x='Skill', color='JobTitle', title='Skill Distribution')

    # Skills per day graph
    skills_df['Date'] = skills_df['DateTime'].dt.date
    fig_skills_per_day = px.histogram(skills_df, x='Date', color='Skill', title='Skills per Day')

    return fig_skills, fig_skills_per_day


if __name__ == '__main__':
    app.run_server(debug=True)
