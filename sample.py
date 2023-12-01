import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from dash_html_components import I

# Load data from the CSV file
df = pd.read_csv('/Users/johngreenough/Library/Containers/com.microsoft.Excel/Data/Desktop/sampledata.csv')  # Replace 'sampledata.csv' with your actual CSV file path

# Extracting additional columns for analysis
df['Time'] = pd.to_datetime(df['Time'])
df['Weekday'] = df['Time'].dt.day_name()
df['Hour'] = df['Time'].dt.hour

# Find the program, course, and hour with the most visits
most_visits_program = df['Program'].value_counts().idxmax()
most_visits_course = df['Course'].value_counts().idxmax()
busiest_hour = df['Hour'].value_counts().idxmax()
total_interactions = len(df)

# Get unique programs and courses
programs = df['Program'].unique()
courses = df['Course'].unique()

# Get unique months
months = df['Time'].dt.month_name().unique()

# App initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define a reusable function to create bar charts
def create_bar_chart(data, x, y, title):
    fig = px.bar(data, x=x, y=y, labels={x: x.capitalize(), y: 'Total Visits'}, title=title)
    return fig

# Define a reusable function to create pie charts
def create_pie_chart(data, names, values, title):
    fig = px.pie(data, names=names, values=values, labels={names: names.capitalize(), values: 'Total Visits'}, title=title)
    return fig

# Define a reusable function to create heatmap charts
def create_heatmap(data, x, y, color, title):
    fig = px.imshow([data[color].value_counts().reindex(y).values], x=x, y=[title], color_continuous_scale='viridis',
                    labels=dict(x=x.capitalize(), y=''), title=title)
    return fig

# App layout
app.layout = dbc.Container(
    fluid=True,
    children=[

        html.H1("Office Visits Analysis", className="display-4 text-center mt-2 mb-4"),
        
        dbc.Row([
            dbc.Col(
                dbc.DropdownMenu(
                    label="Select a program",
                    children=[
                        dbc.DropdownMenuItem(program, id=f"program-dropdown-item-{i}", n_clicks_timestamp=0)
                        for i, program in enumerate(programs)
                    ],
                    id="program-dropdown-top",
                    className="mb-2 dropdown",  # Combine multiple class names
                    color="primary",
                    style={'position': 'relative'},
                ),
            ),
        ]),

        dbc.Row([
            dbc.Col([
                html.P([I(className="fas fa-chart-bar"), f" Program with the Most Visits: {most_visits_program}"], className="lead text-primary"),
                html.P([I(className="fas fa-graduation-cap"), f" Course with the Most Visits: {most_visits_course}"], className="lead text-primary"),
                html.P([I(className="far fa-clock"), f" Busiest Hour: {busiest_hour}:00"], className="lead text-primary"),
                html.P([I(className="far fa-handshake"), f" Total Interactions: {total_interactions}"], className="lead text-info"),
            ], width=12),
        ], className="mb-4"),

        # Dropdown to select a program and month
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='program-dropdown',
                    options=[{'label': program, 'value': program} for program in programs],
                    value=most_visits_program,
                    multi=False,
                    placeholder="Select a program",
                    className="mb-2",
                    style={'position': 'relative'}
                ),
                width=6
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in months],
                    value=months[0],
                    multi=False,
                    placeholder="Select a month",
                    className="mb-2",
                    style={'position': 'relative'}
                ),
                width=6
            )
        ], className="mb-4"),

        # Graphs
        dbc.Row([
            dbc.Col(dcc.Graph(id='program-bar'), width=6),
            dbc.Col(dcc.Graph(id='program-pie'), width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='course-bar'), width=6),
            dbc.Col(dcc.Graph(id='weekday-heatmap'), width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='hour-bar'), width=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='total-students-vs-visits'), width=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='interactions-scatter'), width=12),
        ], className="mb-4"),
    ]
)

# Callbacks
@app.callback(
    Output('program-bar', 'figure'),
    Output('program-pie', 'figure'),
    Output('course-bar', 'figure'),
    Output('weekday-heatmap', 'figure'),
    Output('hour-bar', 'figure'),
    Output('total-students-vs-visits', 'figure'),
    Output('interactions-scatter', 'figure'),
    Input('program-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('program-dropdown-top', 'n_clicks_timestamp'),
    [Input(f"program-dropdown-item-{i}", 'n_clicks_timestamp') for i in range(len(programs))]
)
def update_graphs(selected_program, selected_month, top_dropdown_timestamp, *item_timestamps):
    ctx = dash.callback_context

    # Determine which program was clicked in the top dropdown
    if ctx.triggered_id == 'program-dropdown-top':
        clicked_program_index = item_timestamps.index(max(item_timestamps))
        selected_program = programs[clicked_program_index]

    # Filter the data based on the selected program and month
    filtered_df = df[(df['Program'] == selected_program) & (df['Time'].dt.month_name() == selected_month)]

    # Visualization 1: Total Visits by Program (Bar Graph)
    program_bar = create_bar_chart(filtered_df['Program'].value_counts().reset_index(), 'index', 'Program',
                                   f'Total Visits by Program ({selected_program}, {selected_month})')

    # Visualization 2: Proportion of Student Visits by Program (Pie Chart)
    program_pie = create_pie_chart(filtered_df['Program'].value_counts().reset_index(), 'index', 'Program',
                                   f'Proportion of Student Visits by Program ({selected_program}, {selected_month})')

    # Visualization 3: Total Visits by Course (Bar Chart)
    course_bar = create_bar_chart(filtered_df['Course'].value_counts().reset_index(), 'index', 'Course',
                                   f'Total Visits by Course ({selected_program}, {selected_month})')

    # Visualization 4: Busiest Weekday (Heatmap)
    weekday_heatmap = create_heatmap(filtered_df, 'Weekday', ['Busiest Weekday'], 'Busiest Weekday',
                                     f'Busiest Weekday ({selected_program}, {selected_month})')

    # Visualization 5: Busiest Hour (Bar Chart)
    hour_bar = create_bar_chart(filtered_df['Hour'].value_counts().sort_index().reset_index(), 'index', 'Hour',
                                f'Busiest Hour ({selected_program}, {selected_month})')

    # Visualization 6: Total Students vs Total Visits by Program (Bar Graph)
    total_students_vs_visits = create_bar_chart(filtered_df['Program'].value_counts().reset_index(), 'index', 'Program',
                                                 f'Total Students vs Total Visits by Program ({selected_program}, {selected_month})')

    # Visualization 7: Interactions Scatter Plot
    interactions_scatter = px.scatter(filtered_df, x='Time', y='Interactions',
                                      labels={'Time': 'Date', 'Interactions': 'Total Interactions'},
                                      title=f'Total Interactions by Day ({selected_program}, {selected_month})')

    return program_bar, program_pie, course_bar, weekday_heatmap, hour_bar, total_students_vs_visits, interactions_scatter

if __name__ == '__main__':
    app.run_server(debug=True)
