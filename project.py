import pandas as pd
import dash
import dash_html_components as html
from  dash.dependencies import Input,Output,State
import webbrowser
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px 
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

def load_data():
    data = "glob.csv"

    
    #********************************global_variable************************************************

    global df, month_list,date_list,region_list,country_list,state_list,city_list,cdd_values,attack_type_list,year_list,year_dict
    df = pd.read_csv(data)
  
    global month
    month={'January':1,
           'February':2,
           'March:':3,
           'April':4,
           'May':5,
           'June':6,
           'July':7,
           'August':8,
           'September':9,
           'October':10,
           'November':11,
           'December':12}


  
    #****************************************data_from_dataset*************************************




    month_list= [{"label":key, "value":values} for key,values in month.items()] 
    date_list = [x for x in range(1, 32)]
    region_list=[{'label':str(i),'value':str(i)} for i in sorted(df['region_txt'].unique().tolist())] 
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    city_list=df.groupby("provstate")["city"].unique().apply(list).to_dict()
    attack_type_list= [{'label':str(i),'value':str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    year_list=  sorted(df['iyear'].unique().tolist())
    year_dict= {str(i):str(i) for i in year_list }






    cdd_val = {"Terrorist Organisation":'gname',
                  "Target Nationality":'natlty1_txt', 
                  "Target Type":'targtype1_txt', 
                  "Type of Attack":'attacktype1_txt', 
                  "Weapon Type":'weaptype1_txt', 
                  "Region":'region_txt', 
                  "Country Attacked":'country_txt'
                          }
                
    cdd_values = [{"label":keys, "value":value} for keys, value in cdd_val.items()]
  
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/') #chk address


def create_app_ui():
    layout=html.Div([html.H1(
                    id='main_title',
                    children='Terror analysis and Insights',className='banner'),


                   dcc.Tabs(
        id="Tabs",
        value="Map",
        children=[dcc.Tab(label="Map tool" ,id="Map tool",value="Map", 
                        children=[dcc.Tabs(id = "subtabs", value = "WorldMap",
                                           children = [
                                                dcc.Tab(label="World map", id="map_World", value="WorldMap"),
                                                dcc.Tab(label="India map", id="map_India", value="IndiaMap")
                                                ]),
                                               
    dcc.Dropdown(id='month-dropdown',options= month_list,placeholder='Select month',multi=True,className='drop'),
    dcc.Dropdown(id='date-dropdown',options= date_list,placeholder='Select date',multi=True,className='drop'),
    dcc.Dropdown(id='region-dropdown',options= region_list,placeholder='Select region',multi=True,className="drop"),
    dcc.Dropdown(id='country-dropdown',  options=country_list,value='India',placeholder='Select country',multi=True,className='drop'),
    dcc.Dropdown(id='state-dropdown',options= state_list,placeholder='Select state/province',multi=True,className='drop'),
    dcc.Dropdown(id='city-dropdown',options= city_list,placeholder='Select city',multi=True,className='drop'),
    dcc.Dropdown(id='attacktype-dropdown',options=attack_type_list,placeholder='Select attack type',multi=True,className='drop'),
                    
    html.H4('Select Year range', id='year-range'),
      
    dcc.RangeSlider(
        id='year-slider',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict,
        step=None),
    html.Br()
    ]),
     
    dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "Wo-Chart",children = [
              dcc.Tab(label="World-Chart-tool", id="chart-world", value="WorldChart"),          
              dcc.Tab(label="India-Chart-tool", id="chart-India", value="IndiaChart")]),
            dcc.Dropdown(id="Chart-Dropdown", options = cdd_values, placeholder="Select option", value = "region_txt"), 
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Hr(),
            dcc.RangeSlider(
                id='year-slider1',
                min=min(year_list),
                max=max(year_list),
                value=[min(year_list),max(year_list)],
                marks=year_dict,
                step=None),
            html.Br()
         ]),
           ]),
    html.Div(id = "graph-object", children ="waiting for map")
      ])
        
    return layout


@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
    dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month-dropdown', 'value'),
    dash.dependencies.Input('date-dropdown', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('year-slider1', 'value'), 
    dash.dependencies.Input("Chart-Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")
    ]
    )

def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        
        
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        #month
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value) & (new_df["iday"].isin(date_value))]
        
        # state
        
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)



@app.callback(
  Output("date-dropdown", "options"),
  [Input("month-dropdown", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),  #for only india case 
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

def main():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app_ui()
  app.title = "Terrorism Analysis with Insights"
  app.css.append_css(
        {'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})
  app.run_server()
  df = None #Memory saving 
  app = None


if __name__ == '__main__':
    main()
