# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = [{'label':'All Sites', 'value':'ALL'}]
for site in spacex_df['Launch Site'].unique():
    sites.append({'label':site, 'value':site})
marks = {}
for i in range(int(min_payload), int(max_payload), 1000):
    marks[str(i)] = i

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(html.H3('Launch Sites', style={'margin-right': '2em'})),
                                dcc.Dropdown(id='site-dropdown', options = sites, value='ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', figure=[])),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, step=100, marks=marks,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', figure=[])),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

#Place to add @app.callback Decorator
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class']==1].groupby(['Launch Site'], as_index=False).count()
    if entered_site == 'ALL':
        #fig = px.bar(filtered_df, x='Launch Site', y='Payload Mass (kg)', title="Pie")
        fig = px.pie(filtered_df, values='class', names='Launch Site',
        title='Total success launches all sites')
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['class'], as_index=False).count()
        
        fig = px.pie(filtered_df, values='Launch Site', names='class', title="Total Success Launches for site "+str(entered_site))

    return fig

   
   
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

#Place to add @app.callback Decorator
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, interval_value):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=interval_value[0]) & (spacex_df['Payload Mass (kg)']<=interval_value[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
        title='Correlation between Payload and Sucess for all Sites in Range of '+str(interval_value[0])+" to "+str(interval_value[1])+" Payload Mass")
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>=interval_value[0])
         & (spacex_df['Payload Mass (kg)']<=interval_value[1])]        
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
        title='Correlation between Payload and Sucess for '+str(entered_site)+' in Range of '+str(interval_value[0])+" to "+str(interval_value[1])+" Payload Mass")
        
    return fig

   

# Run the app
if __name__ == '__main__':
    app.run_server()
