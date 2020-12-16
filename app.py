import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_table

import plotly.express as px

df = px.data.gapminder()

df_filt = df.loc[df.year==2007 , ["country", "continent", "year", "lifeExp", "pop", "gdpPercap"]]
df_filt['lifeExp'] = round(df_filt['lifeExp'], 2)
df_filt['gdpPercap'] = round(df_filt['gdpPercap'], 2)


figura_2 = px.scatter(df_filt[df_filt.continent.isin(['Europe', 'Americas'])], 
              x="lifeExp", 
              y="pop", 
              color='continent',
              size='gdpPercap',
              hover_name="country",
              labels={'lifeExp':'Expectativa de vida', 
                      'pop':'Población', 
                      'gdpPercap':'PBI per cápita'},
              title='Pbi per cápita y expectativa de vida (2007)'
              )

#App
app = dash()

#Layout
app.layout = html.Div([
    dcc.Dropdown(id='dropdown_1', 
                 options=[
                     {'label':'America', 'value':'Americas'},
                     {'label':'Europe', 'value':'Europe'}], 
                 value=['Americas', 'Europe'], 
                 multi=True),
     dcc.Graph(id='grafico',figure=figura_2), 
     dash_table.DataTable(
                     id='tabla',
                     data=df_filt.to_dict('records'),
                     columns=[{'name': i, 'id': i } for i in df_filt.columns ],
                     style_header={'backgroundColor': 'steelblue', 'color':'white'},
                     style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue'},
                     filter_action='native', 
                     page_current= 0,
                     page_size= 10,
                    )
     
]) 



@app.callback(
    Output(component_id='grafico', component_property='figure'),
    [Input(component_id='dropdown_1', component_property='value')]
)

def update_grafico(selected_values):

    figura_2 = px.scatter(df_filt[df_filt.continent.isin(selected_values)], 
              x="lifeExp", 
              y="pop", 
              color='continent',
              size='gdpPercap',
              hover_name="country",
              labels={'lifeExp':'Expectativa de vida', 
                      'pop':'Población', 
                      'gdpPercap':'PBI per cápita'},
              title='Pbi per cápita y expectativa de vida (2007)'
              )

    return figura_2

# DATATABLE
@app.callback(
    Output(component_id='tabla', component_property='data'),
    [Input(component_id='dropdown_1', component_property='value')]
)


def update_datatable(selected_values):

    df_continente_seleccionado = df_filt[df_filt.continent.isin(selected_values)]

    data_tabla_continente_seleccionado = df_continente_seleccionado.to_dict('records')

    return data_tabla_continente_seleccionado




#Ejecutar
if __name__ == '__main__':
    app.run_server() 
