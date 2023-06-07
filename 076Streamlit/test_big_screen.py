from streamlit_echarts import st_echarts
import streamlit as st

st.set_page_config(layout="wide")

col1, col2, col3, col4, col5 = st.columns([0.2, 1, 0.2, 1, 0.2])

with col1:
    st.empty()
with col2:
    option = {
        "tooltip": {
            "formatter": '{a} <br/>{b} : {c}%'
        },
        "series": [{
            "name": '进度',
            "type": 'gauge',
            "startAngle": 180,
            "endAngle": 0,
            "progress": {
                "show": "true"
            },
            "radius": '100%',

            "itemStyle": {
                "color": '#58D9F9',
                "shadowColor": 'rgba(0,138,255,0.45)',
                "shadowBlur": 10,
                "shadowOffsetX": 2,
                "shadowOffsetY": 2,
                "radius": '55%',
            },
            "progress": {
                "show": "true",
                "roundCap": "true",
                "width": 15
            },
            "pointer": {
                "length": '60%',
                "width": 8,
                "offsetCenter": [0, '5%']
            },
            "detail": {
                "valueAnimation": "true",
                "formatter": '{value}%',
                "backgroundColor": '#58D9F9',
                "borderColor": '#999',
                "borderWidth": 4,
                "width": '60%',
                "lineHeight": 20,
                "height": 20,
                "borderRadius": 188,
                "offsetCenter": [0, '40%'],
                "valueAnimation": "true",
            },
            "data": [{
                "value": 66.66,
                "name": '百分比'
            }]
        }]
    };

    st_echarts(options=option, key="1")

    option = {
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "top": '5%',
            "left": 'center'
        },
        "series": [
            {
                "name": '访问来源',
                "type": 'pie',
                "radius": ['40%', '75%'],
                "avoidLabelOverlap": "false",
                "itemStyle": {
                    "borderRadius": "10",
                    "borderColor": '#fff',
                    "borderWidth": "2"
                },
                "label": {
                    "show": "false",
                    "position": 'center'
                },
                "emphasis": {
                    "label": {
                        "show": "true",
                        "fontSize": '20',
                        "fontWeight": 'bold'
                    }
                },
                "labelLine": {
                    "show": "true"
                },
                "data": [
                    {"value": 1048, "name": '搜索引擎'},
                    {"value": 735, "name": '直接访问'},
                    {"value": 580, "name": '邮件营销'},
                    {"value": 484, "name": '联盟广告'},
                    {"value": 300, "name": '视频广告'}
                ]
            }
        ]
    };

    st_echarts(options=option, key="2")

with col3:
    st.empty()

with col4:
    option = {
        "legend": {
            "top": 'top'
        },
        "toolbox": {
            "show": "true",
            "feature": {
                "mark": {"show": "true"},
                "dataView": {"show": "true", "readOnly": "false"},
                "restore": {"show": "true"},

            }
        },
        "series": [
            {
                "name": '面积模式',
                "type": 'pie',
                "radius": ["30", "120"],
                "center": ['50%', '60%'],
                "roseType": 'area',
                "itemStyle": {
                    "borderRadius": "8"
                },
                "data": [
                    {"value": 40, "name": '苹果'},
                    {"value": 38, "name": '梨子'},
                    {"value": 32, "name": '香蕉'},
                    {"value": 30, "name": '桃子'},
                    {"value": 28, "name": '葡萄'},
                    {"value": 26, "name": '芒果'},
                    {"value": 22, "name": '李子'},
                    {"value": 18, "name": '菠萝'}
                ]
            }
        ],
        "tooltip": {
            "show": "true"
        },
        "label": {
            "show": "true"
        },
    };

    st_echarts(options=option, key="3")

    option = {
        "toolbox": {
            "show": "true",
            "feature": {
                "dataZoom": {
                    "yAxisIndex": "none"
                },
                "dataView": {
                    "readOnly": "false"
                },
                "magicType": {
                    "type": ["line", "bar"]
                },
                "restore": {"show": "true"},
            }
        },
        "xAxis": {
            "type": 'category',
            "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [{
            "data": [
                {"value": 900, "itemStyle": {"color": "#FF0000"}},
                {"value": 750, "itemStyle": {"color": "#FF7D00"}},
                {"value": 520, "itemStyle": {"color": "#FFFF00"}},
                {"value": 350, "itemStyle": {"color": "#00FF00"}},
                {"value": 200, "itemStyle": {"color": "#0000FF"}},
                {"value": 130, "itemStyle": {"color": "#00FFFF"}},
                {"value": 70, "itemStyle": {"color": "#FF00FF"}},
            ],
            "type": 'bar'

        }],
        "tooltip": {
            "show": "true"
        },
        "label": {
            "show": "true"
        },

    };
    st_echarts(options=option, key="4")

with col5:
    st.empty()
