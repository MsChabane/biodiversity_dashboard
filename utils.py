import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

months=['January','February','March','April','May','June','July','August','September','October','November','December']

def generate_kingdom_plot(df:pd.DataFrame):
    top10 = df["kingdom"].value_counts().reset_index().iloc[:10]
    top10.columns = ["kingdom","count"]
    fig = px.bar(top10, x="kingdom", y="count",
                title="Top Kingdoms",
                template="plotly_dark")

    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)


    fig.update_traces(marker_line_width=0,
                    marker_opacity=0.8)


    fig.update_traces(marker=dict(
    line=dict(width=2, color="rgba(0,0,0,0.6)"),
        ),
    opacity=0.85,

    )

    fig.update_layout(
        bargap=0.25,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title="", 
        xaxis_title="",
    )

    return fig

def generate_monthly_trend_observation(df:pd.DataFrame):
    fig = go.Figure()
    df_grouped=df.groupby('month').size().reset_index(name='count')
    df_grouped.month=pd.Categorical(df_grouped.month,categories=months,ordered=True)
    df_grouped.sort_values(by='month',inplace=True)
    fig.add_trace(go.Scatter(
        x=df_grouped['month'],
        y=df_grouped['count'],
        mode='lines',
        line=dict(color='cyan', width=3),
        fill='tozeroy',         
        fillcolor='rgba(0,255,255,0.2)' 
    ))

    fig.update_layout(
        template='plotly_dark',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(line_shape='spline',line=dict(width=1),fill='tozeroy', fillcolor='rgba(0, 255, 255, 0.1)')
    return fig

def generate_tree_map(df:pd.DataFrame):
    fig = px.treemap(
    df,
    path=['kingdom','phylum','class'],
    title="",
    template='plotly_dark',
    color_discrete_sequence=['#FDE2E1', '#E5F7E6']
)

   
    fig.update_traces(
        hovertemplate='',
        marker=dict(
            line=dict(width=1)  
        )
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=50)
    )

    return fig

def generate_obs_dist_map(df:pd.DataFrame):
    fig = px.scatter_map(
        df,
        lat='decimalLatitude',
        lon='decimalLongitude',
        labels='kingdom',
        zoom=4,
        template='plotly_dark'
    )


    fig.update_layout(
        mapbox_style="carto-darkmatter",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=0, r=0, b=0),
        title=""
    )

    return fig

def  generate_monthly_ndvi_trend(p:pd.DataFrame):
    p.month=pd.Categorical(p.month,categories=months,ordered=True)
    p.sort_values(by='month',inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=p['month'],
        y=p[0],
        mode='lines',
        line=dict(color='cyan', width=3),
        fill='tozeroy',         
        fillcolor='rgba(0,255,255,0.2)' 
    ))

    fig.update_layout(
        template='plotly_dark',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(line_shape='spline',line=dict(width=1),fill='tozeroy', fillcolor='rgba(0, 255, 255, 0.1)')
    return fig

def generate_ndvi_per_wilaya(d:pd.DataFrame):
    d.index=pd.Categorical(d.index,categories=months,ordered=True)
    d.sort_index(inplace=True)
    fig=px.imshow(d,color_continuous_scale="Greens",range_color=(0,1))
    fig.update_layout(
        template='plotly_dark',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def generate_yearly_ndvi_per_wilaya(t:pd.DataFrame,geo):
    fig = px.choropleth_mapbox(
    t,
    geojson=geo,
    locations='code',
    featureidkey='properties.code',
    color=0,
    range_color=(0,1),
    color_continuous_scale='Greens',
    mapbox_style="carto-positron",
    zoom=4,
    center={"lat": 28.0, "lon": 2.5},
)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        template='plotly_dark',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig







