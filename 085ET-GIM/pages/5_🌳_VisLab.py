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
import math

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
    menu = ["3D-Building", "GeoMap", "ArcLayer", "Demo", "FlightsLine", "GlobeView", "3D巡航可视化", "星云图"]
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
        df = pd.read_csv("D:/Code/Crawler4Caida/085ET-GIM/data/heatmap-data.csv")
        print(df.to_dict(orient="records"))

        layer_hexagon = pdk.Layer(
            'GridLayer',  # `type` positional argument is here, CPUGridLayer, HexagonLayer,GridLayer
            df,
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

        # 添加文字图层
        # TEXT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"  # noqa
        # df_text = pd.read_json(TEXT_LAYER_DATA)
        text_map = [{"name": 'Colma (COLM)', "address": '365 D Street, Colma CA 94014', "coordinates": [-122.466233, 37.684638]}]
        layer_textmap = pdk.Layer(
            "TextLayer",
            text_map,
            pickable=True,
            get_position="coordinates",
            get_text="name",
            get_size=32,
            get_color=[255, 255, 255],
            get_angle=0,
            get_text_anchor=String('middle'),
            get_alignment_baseline=String('center')
        )
        # 添加旅行路线图层
        TRIPS_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.trips.json"  # noqa
        df = pd.read_json(TRIPS_LAYER_DATA)
        df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
        df["timestamps"] = df["waypoints"].apply(lambda f: [item["timestamp"] - 1554772579000 for item in f])
        df.drop(["waypoints"], axis=1, inplace=True)
        print(df)

        layer_trips = pdk.Layer(
            "TripsLayer",
            df,
            get_path="coordinates",
            get_timestamps="timestamps",
            get_color=[253, 128, 93],
            opacity=0.9,
            width_min_pixels=5,
            rouded=True,
            trail_length=600,
            current_time=500

        )

        # 添加散点图层（可针对单独点做更多的设置）
        # SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
        # df = pd.read_json(SCATTERPLOT_LAYER_DATA)
        # df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))
        # layer_scatter_bart = pdk.Layer(
        #     "ScatterplotLayer",
        #     df,
        #     pickable=True,
        #     opacity=0.8,
        #     stroked=True,
        #     filled=True,
        #     radius_scale=6,
        #     radius_min_pixels=1,
        #     radius_max_pixels=100,
        #     line_width_min_pixels=1,
        #     get_position="coordinates",
        #     get_radius="exits_radius",
        #     get_fill_color=[255, 140, 0],
        #     get_line_color=[0, 0, 0],
        # )

        # 添加路径图层
        DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-lines.json"
        df = pd.read_json(DATA_URL)

        def hex_to_rgb(h):
            h = h.lstrip("#")
            return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))

        df["color"] = df["color"].apply(hex_to_rgb)
        layer_path = pdk.Layer(
            type="PathLayer",
            data=df,
            pickable=True,
            get_color="color",
            width_scale=20,
            width_min_pixels=2,
            get_path="path",
            get_width=5,
        )
        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=-1.415,
            latitude=52.2323,
            zoom=6,
            min_zoom=0,
            max_zoom=22,
            pitch=40.5,
            bearing=-27.36)

        # Combined all of it and render a viewport
        r = pdk.Deck(map_style=map_style,
                     layers=[layer_hexagon, layer_heatmap, layer_scatter, layer_textmap, layer_trips, layer_path],
                     initial_view_state=view_state,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}\n{address}',
                         'style': {
                             'color': 'white'
                         },
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
            max_zoom=22,
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
    elif choice == "FlightsLine":
        DATA_URL = {
            "AIRPORTS": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/airports.json",
            "FLIGHT_PATHS": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/line/heathrow-flights.json",
            # noqa
        }


        # RGBA value generated in Javascript by deck.gl's Javascript expression parser

        GET_COLOR_JS = [
            "255 * (1 - (start[2] / 10000) * 2)",
            "128 * (start[2] / 10000)",
            "255 * (start[2] / 10000)",
            "255 * (1 - (start[2] / 10000))",
        ]

        scatterplot = pdk.Layer(
            "ScatterplotLayer",
            DATA_URL["AIRPORTS"],
            radius_scale=20,
            get_position="coordinates",
            get_fill_color=[255, 140, 0],
            get_radius=60,
            pickable=True,
        )

        line_layer = pdk.Layer(
            "LineLayer",
            DATA_URL["FLIGHT_PATHS"],
            get_source_position="start",
            get_target_position="end",
            get_color=GET_COLOR_JS,
            get_width=10,
            highlight_color=[255, 255, 0],
            picking_radius=10,
            auto_highlight=True,
            pickable=True,
        )

        layers = [scatterplot, line_layer]
        INITIAL_VIEW_STATE = pdk.ViewState(latitude=47.65, longitude=7, zoom=4.5, max_zoom=22, pitch=50, bearing=0)

        r = pdk.Deck(map_style=map_style,
                     layers=layers,
                     initial_view_state=INITIAL_VIEW_STATE,
                     tooltip={
                         # 'html': '<b>Elevation Value:</b> {elevationValue}',
                         'text': '{name}\n{address}',
                         'style': {
                             'color': 'white'
                         },
                     }
                     )
        st.pydeck_chart(r)
    elif choice == "GlobeView":
        COUNTRIES = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson"
        # POWER_PLANTS = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/global_power_plant_database.csv"
        df = pd.read_csv("D:/Code/Crawler4Caida/085ET-GIM/data/global_power_plant_database.csv")
        # COUNTRIES = "D:/Code/Crawler4Caida/085ET-GIM/data/ne_50m_admin_0_scale_rank.geojson"
        # st.write("log1....")

        def is_green(fuel_type):
            """Return a green RGB value if a facility uses a renewable fuel type"""
            if fuel_type.lower() in ("nuclear", "water", "wind", "hydro", "biomass", "solar", "geothermal"):
                return [10, 230, 120]
            return [230, 158, 10]

        df["color"] = df["primary_fuel"].apply(is_green)
        df.drop("wepp_id", axis=1, inplace=True)
        df.drop('year_of_capacity_data', axis=1, inplace=True)
        df.drop('geolocation_source', axis=1, inplace=True)
        df.drop('generation_gwh_2013', axis=1, inplace=True)
        df.drop('generation_gwh_2014', axis=1, inplace=True)
        df.drop('generation_gwh_2015', axis=1, inplace=True)
        df.drop('generation_gwh_2016', axis=1, inplace=True)
        df.drop('generation_gwh_2017', axis=1, inplace=True)
        df.drop('other_fuel1', axis=1, inplace=True)
        df.drop('other_fuel2', axis=1, inplace=True)
        df.drop('other_fuel3', axis=1, inplace=True)
        df.drop('estimated_generation_gwh', axis=1, inplace=True)
        df.drop('url', axis=1, inplace=True)
        df.drop('source', axis=1, inplace=True)
        df.drop('owner', axis=1, inplace=True)
        df.drop('gppd_idnr', axis=1, inplace=True)
        df.drop('country_long', axis=1, inplace=True)
        df.drop('commissioning_year', axis=1, inplace=True)
        # df.drop('capacity_mw', axis=1, inplace=True)

        df_format = df.to_dict(orient="records")
        # print(df_format)
        # st.write("log2....")

        view_state = pdk.ViewState(latitude=51.47, longitude=0.45, zoom=2, min_zoom=1)

        # Set height and width variables
        view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)

        layers = [
            pdk.Layer(
                "GeoJsonLayer",
                id="base-map",
                data=COUNTRIES,
                stroked=False,
                filled=True,
                get_fill_color=[200, 200, 200],
            ),

            pdk.Layer(
                "ColumnLayer",
                id="power-plant",
                data=df_format,
                get_elevation="capacity_mw",
                get_position=["longitude", "latitude"],
                elevation_scale=100,
                pickable=True,
                auto_highlight=True,
                radius=20000,
                get_fill_color="color",
            ),
        ]

        r = pdk.Deck(
            map_style=map_style,
            views=[view],
            initial_view_state=view_state,
            tooltip={"text": "{name}, {primary_fuel} plant, {country}"},
            layers=layers,
            # Note that this must be set for the globe to be opaque
            parameters={"cull": True},
        )
        # r.to_html("globe_view.html", css_background_color="black")
        st.pydeck_chart(r)

else:
    st.info("Please Login!")
