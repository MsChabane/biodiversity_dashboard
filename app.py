from dash import Dash, callback, Output, Input, dcc
import dash_mantine_components as dmc
import pandas as pd
import utils
import numpy as np
import json

ndvi2024 = pd.read_csv("./data/ndvi2024_pivot_table.csv").set_index('month')
ndvi2025 = pd.read_csv("./data/ndvi2025_pivot_table.csv").set_index('month')
occ2025 = pd.read_csv('./data/data_occ_2025.csv')
occ2024 = pd.read_csv('./data/data_occ_2024.csv')
urban_data = pd.read_csv('./data/DZA.csv')
geo = json.load(open("./data/algeria48.geojson"))
with open("./data/code_per_wilaya.json",'r') as f:
     code_per_wilaya = json.load(f)


app = Dash(__name__,title="Algeria Biodiversity Monitoring Dashboard",suppress_callback_exceptions=True)
app.layout = dmc.MantineProvider(
    [
        dmc.Center(
            dmc.Title(
                "🌿 Algeria Biodiversity Monitoring Dashboard (2024 - 2025)",
                order=2,
                style={"color": "#4CAF50"}
            ),
            mt=20
        ),
        dmc.SimpleGrid([
                dmc.Card([dmc.Skeleton(dcc.Graph(id='occ_kpi'),id='occ_kpi_sk',height=300,)], withBorder=True,shadow='md'),
                  dmc.Card([dmc.Skeleton(dcc.Graph(id='max_ndvi_kpi'),id='max_ndvi_kpi_sk',height=300)], withBorder=True,shadow='md'),
                dmc.Card([dmc.Skeleton(dcc.Graph(id='avg_ndvi_kpi'),id='avg_ndvi_kpi_sk',height=300)], withBorder=True,shadow='md'),
                dmc.Card([dmc.Skeleton(dcc.Graph(id='min_ndvi_kpi'),id='min_ndvi_kpi_sk',height=300)], withBorder=True,shadow='md'),
                dmc.Card([dmc.Skeleton(dcc.Graph(id='urban_kpi'),id='urban_kpi_sk',height=300)], withBorder=True,shadow='md'),
                 
        ], mt=20, px=20, cols=5),

       
        dmc.Box(
            [
                
                dmc.Card([
                dmc.Text("Select Year", fw=700, size="lg", c="green"),
                dmc.Select(
                    id="year_selector",
                    data=[{"value": "2024", "label": "2024"},
                          {"value": "2025", "label": "2025"}],
                    value="2025",
                    clearable=False,
                    radius="xl",
                    mt=10,
                    styles={"input": {"textAlign": "center"}}
                )
            ],
            withBorder=True,
            radius="lg",
            shadow="lg",
            style={"width": "300px", "textAlign": "center"}
            ),
              
            ],

            mt=30,px=20
        ),

       
        dmc.Grid([

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Monthly Observation Trend", fw=700, size="lg", c="green"),
                    dmc.Skeleton(dcc.Graph(id='monthly_obs_trend_fig'),
                                 id='monthly_obs_trend_fig_sk', height=500),
                ], withBorder=True, shadow="md", radius="lg"),
                span=4
            ),

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Observation Distribution Map", fw=700, size="lg", c="green"),
                    dmc.Skeleton(dcc.Graph(id='obs_dist_map'),
                                 id='obs_dist_map_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=8
            )

        ], mt=30, px=20),


        # ===== NDVI SECTION ===== #
        dmc.Grid([

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("NDVI per Wilaya", fw=700, size="lg", c="#8BC34A"),
                    dmc.Skeleton(dcc.Graph(id='ndvi_alg'),
                                 id='ndvi_alg_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=8
            ),

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Monthly NDVI Trend", fw=700, size="lg", c="#8BC34A"),
                    dmc.Skeleton(dcc.Graph(id='monthly_ndvi_trend'),
                                 id='monthly_ndvi_trend_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=4
            )

        ], mt=30, px=20),


        # ===== HEATMAP ===== #
        dmc.Grid(
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("NDVI Heatmap Across Wilayas", fw=700, size="lg", c="#689F38"),
                    dmc.Skeleton(dcc.Graph(id='heatmap_fig'),
                                 id='heatmap_fig_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
            ),
            mt=30, px=20
        ),


        # ===== KINGDOM + TREEMAP ===== #
        dmc.Grid([

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Species Kingdom Distribution", fw=700, size="lg", c="#4CAF50"),
                    dmc.Skeleton(dcc.Graph(id='kingdom_fig'),
                                 id='kingdom_fig_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=4
            ),

            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Biodiversity TreeMap", fw=700, size="lg", c="#4CAF50"),
                    dmc.Skeleton(dcc.Graph(id='treemap_fig'),
                                 id='treemap_fig_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=8
            )

        ], mt=30, px=20)
        ,dmc.Grid(
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Urban Population", fw=700, size="lg", c="#4CAF50"),
                    dmc.Skeleton(dcc.Graph(id='urban_line_fig'),
                                 id='urban_line_fig_sk', height=500)
                ], withBorder=True, shadow="md", radius="lg"),
                span=8,offset=2
            )
        )

    ],
    defaultColorScheme="light",
)



@callback(
    [ Output('monthly_obs_trend_fig', 'figure'),
     Output('obs_dist_map', 'figure'),
    Output('ndvi_alg', 'figure'),
     Output('monthly_ndvi_trend', 'figure'),
     Output('heatmap_fig', 'figure'),
    Output('kingdom_fig', 'figure'),
    Output('treemap_fig', 'figure'),
    Output('occ_kpi', 'figure'),
    Output('min_ndvi_kpi', 'figure'),
    Output('max_ndvi_kpi', 'figure'),
    Output('avg_ndvi_kpi', 'figure'),
    Output('urban_kpi', 'figure'),
    Output('urban_line_fig', 'figure')

     ],
    [Input('year_selector', 'value')]
)
def render_figures(year_selected):
    year_selected=int(year_selected)
    percent_recent=urban_data[urban_data['Year']==year_selected].Percent.values[0]
    percent_priv=urban_data[urban_data['Year']==year_selected-1].Percent.values[0]

    
    
    if year_selected == 2025:
        data_occ = occ2025
        d = ndvi2025
        total_occ_recent=len(occ2025)
        total_occ_priv=len(occ2024)
        
        
    else :
        data_occ = occ2024
        d = ndvi2024
        total_occ_recent=len(occ2024)
        total_occ_priv=None  

    
    p = d.mean(axis=1).reset_index()
    t = d.mean(axis=0).reset_index()
    t.columns = ['wilaya', 'ndvi']
    t['code']= t.wilaya.map(code_per_wilaya)
    p.columns = ['month', 'ndvi']
    min_ndvi_recent=t.ndvi.min()
    max_ndvi_recent=t.ndvi.max()
    avg_ndvi_recent=t.ndvi.mean()
    min_ndvi_priv=None
    max_ndvi_priv=None
    avg_ndvi_priv=None
    if year_selected == 2025:
        d_priv = ndvi2024
        t_priv = d_priv.mean(axis=0).reset_index()
        t_priv.columns = ['wilaya', 'ndvi']
        min_ndvi_priv=t_priv.ndvi.min()
        max_ndvi_priv=t_priv.ndvi.max()
        avg_ndvi_priv=t_priv.ndvi.mean()
    
    figure_monthly_tred=utils.generate_monthly_trend_observation(data_occ)
    figure_treemap=utils.generate_tree_map(data_occ)
    fig_king= utils.generate_kingdom_plot(data_occ)
    figure_dist_map=utils.generate_obs_dist_map(data_occ)
    heatmap = utils.generate_ndvi_per_wilaya(d)
    monthly_trend = utils.generate_monthly_ndvi_trend(p)

    occ_kpi=utils.make_indicator(total_occ_recent,total_occ_priv,"Total Observations",[10000,50000])
    min_ndvi_kpi=utils.make_indicator(round(min_ndvi_recent,4),round(min_ndvi_priv,4) if min_ndvi_priv else None,"Min NDVI",[0,1])
    max_ndvi_kpi=utils.make_indicator(round(max_ndvi_recent,4),round(max_ndvi_priv,4) if max_ndvi_priv else None,"Max NDVI",[0,1])
    avg_ndvi_kpi=utils.make_indicator(round(avg_ndvi_recent,4),round(avg_ndvi_priv,4) if avg_ndvi_priv else None,"Avg NDVI",[0,1])
    urban_kpi=utils.make_indicator(percent_recent,percent_priv,"Urban Area Percentage",[0,100])
    
    alg_fig = utils.generate_yearly_ndvi_per_wilaya(t, geo)
    urban_line_fig=utils.generate_urban_rate(urban_data)

    return (figure_monthly_tred
            ,figure_dist_map,
            alg_fig, 
            monthly_trend,
              heatmap,fig_king,
              figure_treemap
              ,occ_kpi,
              min_ndvi_kpi,
              max_ndvi_kpi,
              avg_ndvi_kpi,
              urban_kpi,
              urban_line_fig
              )

@callback(
Output("monthly_obs_trend_fig_sk",'visible'),
    Input('monthly_obs_trend_fig', 'figure'),
)
def a(fig):
    return fig is None or fig == {}
@callback(
Output("obs_dist_map_sk",'visible'),
    Input('obs_dist_map', 'figure'),
)
def b(fig):
    return fig is None or fig == {}
@callback(
Output("ndvi_alg_sk",'visible'),
    Input('ndvi_alg', 'figure'),
)
def c(fig):
    return fig is None or fig == {}
@callback(
Output("monthly_ndvi_trend_sk",'visible'),
    Input('monthly_ndvi_trend', 'figure'),
)
def d(fig):
    return fig is None or fig == {}
@callback(
Output("heatmap_fig_sk",'visible'),
    Input('heatmap_fig', 'figure'),
)
def e(fig):
    return fig is None or fig == {}
@callback(
Output("kingdom_fig_sk",'visible'),
    Input('kingdom_fig', 'figure'),
)
def f(fig):
    return fig is None or fig == {}
@callback(
Output("treemap_fig_sk",'visible'),
    Input('treemap_fig', 'figure'),
)
def f(fig):
    return fig is None or fig == {}

@callback(
Output("occ_kpi_sk",'visible'),
    Input('occ_kpi', 'figure')
)
def g(fig):
    return fig is None or fig == {}

@callback(
Output("min_ndvi_kpi_sk",'visible'),
    Input('min_ndvi_kpi', 'figure')
)
def e(fig):
    return fig is None or fig == {}
@callback(
Output("max_ndvi_kpi_sk",'visible'),
    Input('max_ndvi_kpi', 'figure')
)
def f(fig):
    return fig is None or fig == {}
@callback(
Output("avg_ndvi_kpi_sk",'visible'),
    Input('avg_ndvi_kpi', 'figure')
)
def h(fig):
    return fig is None or fig == {}
@callback(
Output("urban_kpi_sk",'visible'),
    Input('urban_kpi', 'figure')
)
def l(fig):
    return fig is None or fig == {}
@callback(
Output("urban_line_fig_sk",'visible'),
    Input('urban_line_fig', 'figure')
)
def z(fig):
    return fig is None or fig == {}

   

if __name__ == "__main__":
    app.run(debug=False,port=8050,host='0.0.0.0')
