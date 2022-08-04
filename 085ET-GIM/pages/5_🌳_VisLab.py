import streamlit as st
import numpy as np
from st_card import st_card
import pandas as pd
import pydeck as pdk
from pydeck.types import String
import graphviz as graphviz

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Div
from bokeh.palettes import Spectral
from bokeh.plotting import figure

import plotly.express as px


st.set_page_config(
    page_title="VisLab",
    page_icon="world_map",
    layout="wide",
)

# 去除streamlit的原生标记
sys_menu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sys_menu, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.user = "Guest"

# 给侧边栏添加APP版本信息
with st.sidebar:
    st.write("Login:", st.session_state.user)
    st.sidebar.markdown(
        """
        <small> ET-GIM 0.1.0 | Jane 2022 </small>  
        [<img src='http://www.mryu.top/content/templates/start/images/github.png' class='img-fluid' width=25 height=25>](https://github.com/52ai) 
        [<img src='http://www.mryu.top/content/templates/start/images/weibo.png' class='img-fluid' width=25 height=25>](http://weibo.com/billcode) 
         """,
        unsafe_allow_html=True,
    )


if st.session_state.count > 0:
    menu = ["3D-Building", "GeoMap", "ArcLayer", "Demo", "3D巡航可视化", "星云图"]
    map_style_list = ["mapbox://styles/mapbox/dark-v10",
                      "mapbox://styles/mapbox/light-v10",
                      "mapbox://styles/mapbox/streets-v11",
                      "mapbox://styles/mapbox/satellite-v9",
                      "dark",
                      "light",
                      "dark_no_labels",
                      "light_no_labels",
                      ]
    st.sidebar.markdown("")
    choice = st.sidebar.selectbox("请选择可视化样式：", menu)
    map_style = st.sidebar.selectbox("地图样式：", map_style_list)
    if choice == "Demo":
        cols0, cols1, cols2, cols3, cols4 = st.columns([1, 1, 1, 1, 1])
        with cols0:
            st_card('Orders', value=1200, delta=-45, delta_description='since last month')
        with cols1:
            st_card('Competed Orders', value=76.4, unit='%', show_progress=True)
        with cols2:
            st_card('Profit', value=45000, unit='($)', delta=48, use_percentage_delta=True,
                    delta_description='since last year')

        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon'])

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v9',
            initial_view_state=pdk.ViewState(
                latitude=37.76,
                longitude=-122.4,
                zoom=6,
                min_zoom=2,
                max_zoom=15,
                pitch=50,
            ),

            layers=[

                pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position='[lon, lat]',
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),

                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))

        st.markdown("### Bokeh Chart")
        p = figure(
            width=700, height=500, toolbar_location=None,
            title="Black body spectral radiance as a function of frequency")


        def spectral_radiance(nu, T):
            h = 6.626e-34  # Planck constant (Js)
            k = 1.3806e-23  # Boltzman constant (J/K)
            c = 2.9979e8  # Speed of light in vacuum (m/s)
            return (2 * h * nu ** 3 / c ** 2) / (np.exp(h * nu / (k * T)) - 1.0)


        Ts = np.arange(2000, 6001, 500)  # Temperature (K)
        palette = Spectral[len(Ts)]
        nu = np.linspace(0.1, 1e15, 500)  # Frequency (1/s)

        for i, T in enumerate(Ts):
            B_nu = spectral_radiance(nu, T)
            p.line(nu / 1e15, B_nu / 1e-9, line_width=2,
                   legend_label=f"T = {T} K", line_color=palette[i])
        p.legend.items = list(reversed(p.legend.items))

        # Peak radiance line.
        Ts = np.linspace(1900, 6101, 50)
        peak_freqs = Ts * 5.879e10
        peak_radiance = spectral_radiance(peak_freqs, Ts)
        p.line(peak_freqs / 1e15, peak_radiance / 1e-9, line_color="silver",
               line_dash="dashed", line_width=2, legend_label="Peak radiance")

        curdoc().theme = 'dark_minimal'
        p.y_range.start = 0
        p.xaxis.axis_label = r"$$\color{white} \nu \:(10^{15} s^{-1})$$"
        p.yaxis.axis_label = r"$$\color{white} B_\nu(\nu, T) \quad(10^{-9} J s m^{-3})$$"

        div = Div(text=r"""
        A plot of the spectral radiance, defined as a function of the frequency $$\nu$$, is given by the formula
        <p \>
        $$
        \qquad B_\nu(\nu, T) = \frac{2h\nu^3}{c^2} \frac{1}{\exp(h\nu/kT)-1}\ .
        $$
        """)

        st.bokeh_chart(column(p, div), use_container_width=True)

    elif choice == "GeoMap":
        st.markdown("依托pydeck+mapbox开展，地图系统的研究")
        DATA_SOURCE = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
        # DATA_SOURCE = 'https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/fortune_500.csv'

        layer_hexagon = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here
            DATA_SOURCE,
            get_position=['lng', 'lat'],
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=1)

        layer_scatter = pdk.Layer(
            'ScatterplotLayer',  # Change the `type` positional argument here
            DATA_SOURCE,
            get_position=['lng', 'lat'],
            auto_highlight=True,
            get_radius=1000,  # Radius is given in meters
            get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
            pickable=True)

        layer_heatmap = pdk.Layer(
            "HeatmapLayer",
            DATA_SOURCE,
            opacity=0.9,
            get_position=["lng", "lat"],
            # aggregation=String('MEAN'),
            # get_weight="profit / employees > 0 ? profit / employees : 0"
            )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=-1.415,
            latitude=52.2323,
            zoom=6,
            min_zoom=5,
            max_zoom=15,
            pitch=40.5,
            bearing=-27.36)

        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon],
                     initial_view_state=view_state,
                     tooltip={
                         'html': '<b>Elevation Value:</b> {elevationValue}',
                         'style': {
                             'color': 'white'
                         }
                     }
                     )

        st.pydeck_chart(r)
    elif choice == "ArcLayer":

        GREAT_CIRCLE_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/flights.json"  # noqa

        df = pd.read_json(GREAT_CIRCLE_LAYER_DATA)

        # Use pandas to prepare data for tooltip
        df["from_name"] = df["from"].apply(lambda f: f["name"])
        df["to_name"] = df["to"].apply(lambda t: t["name"])

        # Define a layer to display on a map
        layer = pdk.Layer(
            "GreatCircleLayer",
            df,
            pickable=True,
            get_stroke_width=12,
            get_source_position="from.coordinates",
            get_target_position="to.coordinates",
            get_source_color=[64, 255, 0],
            get_target_color=[0, 128, 200],
            auto_highlight=True,
        )

        # Set the viewport location
        view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=1, bearing=0, pitch=0)

        # Render
        r = pdk.Deck(map_style=map_style,
                     layers=[layer],
                     initial_view_state=view_state,
                     tooltip={"text": "{from_name} to {to_name}"}, )
        r.picking_radius = 10
        st.pydeck_chart(r)
    elif choice == "3D-Building":
        st.markdown("依托pydeck+mapbox开展，地图系统的研究，3D Building")

        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon'])

        layer_hexagon = pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,)

        layer_scatter = pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        )

        DATA_SOURCE = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
        layer_hexagon_london = pdk.Layer(
            'HexagonLayer',  # `type` positional argument is here
            DATA_SOURCE,
            get_position=['lng', 'lat'],
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=1)

        layer_scatter_london = pdk.Layer(
            'ScatterplotLayer',  # Change the `type` positional argument here
            DATA_SOURCE,
            get_position=['lng', 'lat'],
            auto_highlight=True,
            get_radius=1000,  # Radius is given in meters
            get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
            pickable=True)

        # Set the viewport location
        view_state = pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            min_zoom=0,
            max_zoom=16,
            pitch=50,)

        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon, layer_scatter, layer_scatter_london, layer_hexagon_london],
                     initial_view_state=view_state,
                     tooltip={
                         'html': '<b>Elevation Value:</b> {elevationValue}',
                         'style': {
                             'color': 'white'
                         }
                     }
                     )

        st.pydeck_chart(r)

else:
    st.info("Please Login!")
