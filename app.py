from dash import Dash, callback, Output, Input, dcc
import dash_mantine_components as dmc
import pandas as pd
import utils
import numpy as np

# Load data (keep at top)
ndvi = pd.read_csv("./data/ndvi.csv")
occurance = pd.read_csv('./data/data_occ.csv')

app = Dash(__name__)

# Generate random KPI values for now
def generate_kpis():
    return {
        "Total Observations": int(occurance.shape[0]),
        "Average NDVI": round(ndvi['vim'].mean(), 2),
        "Number of Wilayas": ndvi['wilaya'].nunique(),
        "Max NDVI": round(ndvi['vim'].max(), 2),
        "Min NDVI": round(ndvi['vim'].min(), 2)
    }

kpis = generate_kpis()

# Mantine layout
app.layout = dmc.MantineProvider(
    [
        dcc.Location(id='path', refresh=False),

        # Year selector + KPI Cards
        dmc.SimpleGrid([
            *[
               
                 dmc.Card([
                        dmc.Text(title, fw=700, size="sm"),
                        dmc.Text(str(value), fw=700, size="xl")
                    ], withBorder=True, p="md", style={"textAlign": "center"})
                 for title, value in kpis.items()
            ]
        ], mt=15, px=10,cols=5),
        dmc.Grid(
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Select Year:", fw=700, size="lg"),
                    dmc.Select(
                        id="year_selector",
                        data=[{"value": "2024", "label": "2024"},
                              {"value": "2025", "label": "2025"}],
                        value=2025,
                        clearable=False,radius=15
                    )
                ], withBorder=True, p="md"), span=4,
            ),mt=15,px=10
        ),
        # Occurrence Graphs
        dmc.Grid([
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Monthly Observation Trend", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='monthly_obs_trend_fig'),id='monthly_obs_trend_fig_sk',height=500 ),
                ], withBorder=True, p="md"), span=4
            ),
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Observation Distribution Map", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='obs_dist_map'),id='obs_dist_map_sk', height=500)
                ], withBorder=True, p="md"), span=8
            )
        ], mt=15, px=10),

        # NDVI Graphs
        dmc.Grid([
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("NDVI per Wilaya", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='ndvi_alg'),id='ndvi_alg_sk', height=500)
                ], withBorder=True, p="md"), span=8
            ),
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Monthly NDVI Trend", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='monthly_ndvi_trend'),id='monthly_ndvi_trend_sk', height=500)
                ], withBorder=True, p="md"), span=4
            )
        ], mt=15, px=10),

        # Heatmap
        dmc.Grid(
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("NDVI Heatmap Across Wilaya", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='heatmap_fig'),id='heatmap_fig_sk', height=500)
                ], withBorder=True, p="md")
            ), mt=15, px=10
        ),

        # Kingdom & TreeMap
        dmc.Grid([
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Kingdom Plot", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='kingdom_fig'),id='kingdom_fig_sk', height=500)
                ], withBorder=True, p="md"), span=4
            ),
            dmc.GridCol(
                dmc.Card([
                    dmc.Text("Tree Map", fw=700, size="lg", mb="sm"),
                    dmc.Skeleton(dcc.Graph(id='treemap_fig'),id='treemap_fig_sk', height=500)
                ], withBorder=True, p="md"), span=8
            )
        ], mt=15, px=10)
    ],
    defaultColorScheme="dark"
)

# Callback to update NDVI graphs and heatmap when year changes
@callback(
    [ Output('monthly_obs_trend_fig', 'figure'),
     Output('obs_dist_map', 'figure'),
    Output('ndvi_alg', 'figure'),
     Output('monthly_ndvi_trend', 'figure'),
     Output('heatmap_fig', 'figure'),
     Output('kingdom_fig', 'figure'),
     Output('treemap_fig', 'figure')
     ],
    [Input('year_selector', 'value')]
)
def render_ndvi(year_selected):
    import json
    data_occ=occurance.query(f"year=={year_selected}")
    figure_dist_map=utils.generate_obs_dist_map(data_occ)
    figure_monthly_tred=utils.generate_monthly_trend_observation(data_occ)
    figure_treemap=utils.generate_tree_map(occurance)
    fig_king= utils.generate_kingdom_plot(occurance)
    geo = json.load(open("./data/algeria48.geojson"))
    code_per_wilaya = {i[1]: i[0] for i in ndvi[['dzcode', 'wilaya']].value_counts().to_dict().keys()}

    
    d = ndvi.query(f"year=={year_selected}").pivot_table(index='month', columns='wilaya', values='vim')

    
    heatmap = utils.generate_ndvi_per_wilaya(d.copy())
    p = d.mean(axis=1).reset_index()
    monthly_trend = utils.generate_monthly_ndvi_trend(p)

    # Yearly NDVI per Wilaya
    t = d.mean(axis=0).reset_index()
    t['code'] = t.wilaya.map(code_per_wilaya)
    t.code = t.code.astype(str).str.zfill(2)
    alg_fig = utils.generate_yearly_ndvi_per_wilaya(t, geo)

    return figure_monthly_tred,figure_dist_map,alg_fig, monthly_trend, heatmap,fig_king,figure_treemap

@callback(
Output("monthly_obs_trend_fig_sk",'visible'),
    Input('monthly_obs_trend_fig', 'figure'),
)
def a(fig):
    return not fig
@callback(
Output("obs_dist_map_sk",'visible'),
    Input('obs_dist_map', 'figure'),
)
def b(fig):
    return not fig
@callback(
Output("ndvi_alg_sk",'visible'),
    Input('ndvi_alg', 'figure'),
)
def c(fig):
    return not fig
@callback(
Output("monthly_ndvi_trend_sk",'visible'),
    Input('monthly_ndvi_trend', 'figure'),
)
def d(fig):
    return not fig
@callback(
Output("heatmap_fig_sk",'visible'),
    Input('heatmap_fig', 'figure'),
)
def e(fig):
    return not fig
@callback(
Output("kingdom_fig_sk",'visible'),
    Input('kingdom_fig', 'figure'),
)
def f(fig):
    return not fig
@callback(
Output("treemap_fig_sk",'visible'),
    Input('treemap_fig', 'figure')
)
def g(fig):
    return not fig


if __name__ == "__main__":
    app.run(debug=True)
