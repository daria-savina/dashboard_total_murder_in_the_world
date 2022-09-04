from dash import Dash, dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Import and clean data (importing csv into pandas)
df = pd.read_csv('data/result.csv')
df['total_murder'] = pd.to_numeric(df['total_murder'])


# App layout
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Список країн за рівнем вбивств'),
        html.H6(children='Матеріал отриман з Вікіпедії за 1995-2011рр.', style={'marginTop': '-15px',
                                                                                'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),

    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.RadioItems(
                                id='my-input',
                                options=["Америка", "Європа", "Африка", "Азія", "Океанія"],
                                value="Європа",
                                inline=True
                            )
                        ]
                    ),
                ],
                className="four columns number-stat-box",
            ),
            html.Div(
                children=[
                    html.Div(id='kpi_sum', children=[],
                             style={'textAlign': 'center', 'fontWeight': 'bold', 'font-size': '38px'}),
                    html.H3('Кількість вбивств',
                            style={'textAlign': 'center', 'color': '#b6cde2', 'font-size': '14px'}),
                ],
                className="three columns number-stat-box"
            ),
            html.Div(
                children=[
                    html.Div(id='kpi_count', children=[],
                             style={'textAlign': 'center', 'fontWeight': 'bold', 'font-size': '38px'}),
                    html.H3('Кількість країн у списку',
                            style={'textAlign': 'center', 'color': '#b6cde2', 'font-size': '14px'}),
                ],
                className="three columns number-stat-box"
            )
        ],
        style={
            'padding': '2rem',
            'border-radius': '10px',
            'display': 'flex',
            'justify-content': 'center',
            'grid-auto-flow': 'column',
            'grid-column-gap': '10px'}
    ),
    html.Div(
        children=[
            dcc.Graph(id='graph',figure={})
        ]),
])

# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='kpi_sum', component_property='children'),
    Output(component_id='kpi_count', component_property='children'),
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='my-input', component_property='value')]
)
def update_figure(value):
    if len(value)>0:
        dff = df[df['continent'] == value]
        total_sum = dff['total_murder'].sum()
        total_count = dff['total_murder'].count()

        container_kpi_sum = "{}".format(total_sum)
        container_kpi_count = "{}".format(total_count)

        fig = go.Figure(data=go.Choropleth(
            locations=dff['iso'],
            z=dff['total_murder'].astype(float),
            colorscale='purp',
            autocolorscale=False,
            text=dff['country'],
            marker_line_color='white'
        ))

        fig.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C',landcolor='#3f4b56',subunitcolor='grey'),
            font={"size": 9, "color": "White"},
            titlefont={"size": 15, "color": "White"},
            margin={"r": 0, "t": 20, "l": 0, "b": 30},
            paper_bgcolor='#4E5D6C',
            plot_bgcolor='#4E5D6C',
        )

        return container_kpi_sum, container_kpi_count, fig
    elif len(value) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
