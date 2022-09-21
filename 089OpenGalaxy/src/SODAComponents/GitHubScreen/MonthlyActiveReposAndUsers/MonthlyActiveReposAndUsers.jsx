import React from "react";
import ReactEchartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts";
import intl from 'react-intl-universal';

import banner from "./banner.png";

class MonthlyActiveReposAndUsers extends React.Component {
  render() {
    if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;
    let xLabel = this.props.data.xLabel;
    let repos_counts = this.props.data.repos_counts;
    let users_counts = this.props.data.users_counts;

    const option = {
      // backgroundColor: '#0e1c47',
      title: {
        show: true,
        text: `{imgBg|${intl.get('MonthlyActiveReposAndUsers_TITLE')}}`,
        left: "center",
        top: 0,
        textStyle: {
          rich: {
            imgBg: {
              fontSize: 16,
              fontWeight: "bold",
              color: "white",
              padding: [0, 20, 0, 30],
              backgroundColor: {
                image: banner,
              },
              height: 50,
            },
          },
        },
      },
      tooltip: {
        trigger: "axis",
        backgroundColor: "transparent",
        borderWidth: 0,
        axisPointer: {
          lineStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: "rgba(126,199,255,0)", // 0% 处的颜色
                },
                {
                  offset: 0.5,
                  color: "rgba(126,199,255,1)", // 100% 处的颜色
                },
                {
                  offset: 1,
                  color: "rgba(126,199,255,0)", // 100% 处的颜色
                },
              ],
              global: false, // 缺省为 false
            },
          },
        },
        formatter: (p) => {
          let dom = `<div style="width: 150px;
	height: 50px;color:#fff;position: relative;">
        <svg style="position: absolute;top: 50%;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);" class="svg" xmlns="http://www.w3.org/2000/svg" width="150" height="71" viewBox="0 0 84 55">
      <defs>
        <style>
          .cls-1 {
            fill: #07172c;
            fill-opacity: 0.8;
            stroke: #a7d8ff;
            stroke-linejoin: round;
            stroke-opacity: 0.2;
            stroke-width: 1px;
            fill-rule: evenodd;
          }

        </style>
      </defs>
      <rect class="cls-1" x="-10" y="5" width="300" height="60">
        transform="translate(-258.5 -592.5)" />
    </svg>
        <div style="padding: 4px 8px 4px 14px;display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;position: relative;z-index: 1;">
            <div style="margin-bottom: 4px;width:100%;display:${
              p[0] ? "flex" : "none"
            };justify-content:space-between;align-items:center;">
                <span style="font-size:14px;color:#7ec7ff;">${
                  p[0] ? p[0].seriesName : ""
                }</span>
                <span style="font-size:14px;color:#fff;">${
                  p[0] ? numFormat(p[0].data, 1) : ""
                }</span>
            </div>
            <div style="width:100%;height:100%;display:${
              p[1] ? "flex" : "none"
            };justify-content:space-between;align-items:center;">
                <span style="font-size:14px;color:#7ec7ff;">${
                  p[1] ? p[1].seriesName : ""
                }</span>
                <span style="font-size:14px;color:#fff;">${
                  p[1] ? p[1].data : ""
                }</span>
            </div>
        </div>
    </div>`;
          return dom;
        },
      },
      legend: {
        align: "left",
        right: "5%",
        top: "14%",
        type: "plain",
        textStyle: {
          color: "#7ec7ff",
          fontSize: 16,
        },
        itemGap: 25,
        itemWidth: 18,
        icon: "path://M0 2a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2z",

        data: [
          {
            name: intl.get('MonthlyActiveReposAndUsers_REPO'),
          },
          {
            name: intl.get('MonthlyActiveReposAndUsers_USER'),
          },
        ],
      },
      grid: {
        top: "22%",
        left: "15%",
        right: "15%",
      },
      xAxis: [
        {
          type: "category",
          boundaryGap: false,
          axisLine: {
            show: true,
            lineStyle: {
              color: "#233653",
            },
          },
          axisLabel: {
            show: true,
            interval: 0,
            textStyle: {
              color: "#7ec7ff",
              padding: 16,
              fontSize: 14,
            },
            formatter: function (data) {
              return `${data}${intl.get('MonthlyActiveReposAndUsers_XAXIS_LABEL_UNIT')}`;
            },
          },
          splitLine: {
            show: true,
            interval: 0,
            lineStyle: {
              color: "#192a44",
            },
          },
          axisTick: {
            show: false,
          },
          data: xLabel,
        },
      ],
      yAxis: [
        {
          id: 0,
          name: "",
          nameTextStyle: {
            color: "#7ec7ff",
            fontSize: 16,
            padding: 10,
          },
          min: 0,
          splitLine: {
            show: true,
            lineStyle: {
              color: "#192a44",
            },
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: "#233653",
            },
          },
          axisLabel: {
            show: true,
            textStyle: {
              color: "#7ec7ff",
              padding: 16,
            },
            formatter: function (value) {
              return numFormat(value, 1);
            },
          },
          axisTick: {
            show: false,
          },
        },
        {
          id: 1,
          name: "",
          position: "right",
          nameTextStyle: {
            color: "#7ec7ff",
            fontSize: 16,
            padding: 10,
          },
          min: 0,
          splitLine: {
            show: true,
            lineStyle: {
              color: "#192a44",
            },
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: "#233653",
            },
          },
          axisLabel: {
            show: true,
            textStyle: {
              color: "#7ec7ff",
              padding: 16,
            },
            formatter: function (value) {
              return numFormat(value, 3);
            },
          },
          axisTick: {
            show: false,
          },
        },
      ],
      series: [
        {
          name: intl.get('MonthlyActiveReposAndUsers_REPO'),
          yAxisIndex: 0,
          type: "line",
          symbol: "circle", // 默认是空心圆（中间是白色的），改成实心圆
          showAllSymbol: true,
          symbolSize: 0,
          smooth: true,
          lineStyle: {
            normal: {
              width: 5,
              color: "rgba(25,163,223,1)", // 线条颜色
            },
            borderColor: "rgba(0,0,0,.4)",
          },
          itemStyle: {
            color: "rgba(25,163,223,1)",
            borderColor: "#646ace",
            borderWidth: 2,
          },
          tooltip: {
            show: true,
          },
          areaStyle: {
            //区域填充样式
            normal: {
              //线性渐变，前4个参数分别是x0,y0,x2,y2(范围0~1);相当于图形包围盒中的百分比。如果最后一个参数是‘true’，则该四个值是绝对像素位置。
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(25,163,223,.3)",
                  },
                  {
                    offset: 1,
                    color: "rgba(25,163,223, 0)",
                  },
                ],
                false
              ),
              shadowColor: "rgba(25,163,223, 0.5)", //阴影颜色
              shadowBlur: 20, //shadowBlur设图形阴影的模糊大小。配合shadowColor,shadowOffsetX/Y, 设置图形的阴影效果。
            },
          },
          data: repos_counts,
        },
        {
          name: intl.get('MonthlyActiveReposAndUsers_USER'),
          yAxisIndex: 1,
          type: "line",
          symbol: "circle", // 默认是空心圆（中间是白色的），改成实心圆
          showAllSymbol: true,
          symbolSize: 0,
          smooth: true,
          lineStyle: {
            normal: {
              width: 5,
              color: "rgba(10,219,250,1)", // 线条颜色
            },
            borderColor: "rgba(0,0,0,.4)",
          },
          itemStyle: {
            color: "rgba(10,219,250,1)",
            borderColor: "#646ace",
            borderWidth: 2,
          },
          tooltip: {
            show: true,
          },
          areaStyle: {
            //区域填充样式
            normal: {
              //线性渐变，前4个参数分别是x0,y0,x2,y2(范围0~1);相当于图形包围盒中的百分比。如果最后一个参数是‘true’，则该四个值是绝对像素位置。
              color: new echarts.graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(10,219,250,.3)",
                  },
                  {
                    offset: 1,
                    color: "rgba(10,219,250, 0)",
                  },
                ],
                false
              ),
              shadowColor: "rgba(10,219,250, 0.5)", //阴影颜色
              shadowBlur: 20, //shadowBlur设图形阴影的模糊大小。配合shadowColor,shadowOffsetX/Y, 设置图形的阴影效果。
            },
          },
          data: users_counts,
        },
      ],
    };

    return (
      <ReactEchartsCore
        echarts={echarts}
        option={option}
        style={{ width, height }}
      />
    );
  }
}

const numFormat = (num, digits) => {
  let si = [
    { value: 1, symbol: "" },
    { value: 1e3, symbol: "k" },
    // { value: 1e6, symbol: "M" },
  ];
  let rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  let i;
  for (i = si.length - 1; i > 0; i--) {
    if (num >= si[i].value) {
      break;
    }
  }
  return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
};

export default MonthlyActiveReposAndUsers;
