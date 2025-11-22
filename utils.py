import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

months=['January','February','March','April','May','June','July','August','September','October','November','December']

def generate_kingdom_plot(df:pd.DataFrame):
    top10 = df["kingdom"].value_counts().reset_index().iloc[:10]
    top10.columns = ["kingdom","count"]
    fig = px.bar(top10, x="kingdom", y="count",
                title="",
                template="plotly_white",
        
        )

    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    fig.update_traces(marker=dict(
    line=dict(width=0, color="#4CAF50"),
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
        line=dict(color='#4CAF50', width=3),
       line_shape='linear',
    ))

    fig.update_layout(
        template='plotly_white',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
  
    return fig

def generate_tree_map(df:pd.DataFrame):
    fig = px.treemap(
    df,
    path=['kingdom','phylum'],
    title="",
    template='plotly_white',
    color_discrete_sequence=["#E0B1AF", "#8AE28E"]
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
        template='plotly_white'
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
        y=p['ndvi'],
        mode='lines',
        line=dict(color='#4CAF50', width=3),
        line_shape='spline'
    ))

    fig.update_layout(
        template='plotly_white',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
   
    return fig

def generate_ndvi_per_wilaya(d:pd.DataFrame):
    d.index=pd.Categorical(d.index,categories=months,ordered=True)
    d.sort_index(inplace=True)
    fig=px.imshow(d,color_continuous_scale="Greens",range_color=(0,1))
    fig.update_layout(
        template='plotly_white',
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
    color='ndvi',
    range_color=(0,1),
    color_continuous_scale='Greens',
    mapbox_style="carto-positron",
    zoom=4,
    center={"lat": 28.0, "lon": 2.5},
)
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        template='plotly_white',
        title="",
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def make_indicator(value,delta,title_text,range): 
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=value,
            delta={'reference': delta},
            title={"text": title_text},
            gauge={

                'axis': {'range': range},
            }
        )
    )

    fig.update_layout(template='plotly_white',
                      plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5, r=5, t=20, b=5),
        height=300,
        
    )
    return fig


def generate_urban_rate(urban:pd.DataFrame):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=urban['Year'],
        y=urban['Urban POP'],

        mode='lines+markers',  
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=8, color='#4CAF50'),
        customdata=urban[['Percent']],

        
        hovertemplate=
        "<b>Year:</b> %{x}<br>" +
        "<b>Urban Population:</b> %{y:,}<br>" +
        "<b>Urban %:</b> %{customdata[0]}%" +
        "<extra></extra>"
    ))

    fig.update_layout(
        template='plotly_white',
        title="",
        xaxis_title="",
        yaxis_title="",
        
        xaxis=dict(
            tickmode='linear',
            tick0=2022,
            dtick=1,
            showgrid=False
        ),

        
        yaxis=dict(
            range=[urban['Urban POP'].min() * 0.998, urban['Urban POP'].max() * 1.0005],
            showgrid=False
        ),
    showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


