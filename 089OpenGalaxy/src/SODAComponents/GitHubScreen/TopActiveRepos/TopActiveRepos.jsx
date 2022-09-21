import React from "react";
import ReactEchartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts";
import intl from 'react-intl-universal';

import banner from "./banner.png";

class TopActiveRepos extends React.Component {
  render() {
    if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;
    let names = this.props.data.names;
    let activities = this.props.data.activities;

    var CubeLeft = echarts.graphic.extendShape({
      shape: {
        x: 0,
        y: 0,
      },
      buildPath: function (ctx, shape) {
        var xAxisPoint = shape.xAxisPoint;
        var c0 = [shape.x, shape.y];
        var c1 = [shape.x - 9, shape.y - 9];
        var c2 = [xAxisPoint[0] - 9, xAxisPoint[1] - 9];
        var c3 = [xAxisPoint[0], xAxisPoint[1]];
        ctx
          .moveTo(c0[0], c0[1])
          .lineTo(c1[0], c1[1])
          .lineTo(c2[0], c2[1])
          .lineTo(c3[0], c3[1])
          .closePath();
      },
    });
    var CubeRight = echarts.graphic.extendShape({
      shape: {
        x: 0,
        y: 0,
      },
      buildPath: function (ctx, shape) {
        var xAxisPoint = shape.xAxisPoint;
        var c1 = [shape.x, shape.y];
        var c2 = [xAxisPoint[0], xAxisPoint[1]];
        var c3 = [xAxisPoint[0] + 18, xAxisPoint[1] - 9];
        var c4 = [shape.x + 18, shape.y - 9];
        ctx
          .moveTo(c1[0], c1[1])
          .lineTo(c2[0], c2[1])
          .lineTo(c3[0], c3[1])
          .lineTo(c4[0], c4[1])
          .closePath();
      },
    });
    var CubeTop = echarts.graphic.extendShape({
      shape: {
        x: 0,
        y: 0,
      },
      buildPath: function (ctx, shape) {
        var c1 = [shape.x, shape.y];
        var c2 = [shape.x + 18, shape.y - 9];
        var c3 = [shape.x + 9, shape.y - 18];
        var c4 = [shape.x - 9, shape.y - 9];
        ctx
          .moveTo(c1[0], c1[1])
          .lineTo(c2[0], c2[1])
          .lineTo(c3[0], c3[1])
          .lineTo(c4[0], c4[1])
          .closePath();
      },
    });
    echarts.graphic.registerShape("CubeLeft", CubeLeft);
    echarts.graphic.registerShape("CubeRight", CubeRight);
    echarts.graphic.registerShape("CubeTop", CubeTop);
    var VALUE = activities;
    var option = {
      title: {
        show: true,
        text: `{imgBg|${intl.get('TopActiveRepos_TITLE')}}`,
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
      grid: {
        left: "5%",
        right: 0,
        bottom: "5%",
        top: "5%",
        containLabel: true,
      },
      xAxis: {
        type: "category",
        data: names,
        axisLine: {
          show: true,
          symbol: ['none', 'arrow'],
          lineStyle: {
            color: "#b1b19c",
          },
        },
        offset: 10,
        axisTick: {
          show: false,
          length: 9,
          alignWithLabel: true,
          lineStyle: {
            color: "#fff",
          },
        },
        axisLabel: {
          fontSize: 14,
          color: "#fff",
          rotate: 35,
        },
      },
      yAxis: {
        type: "value",
        axisLine: {
          show: true,
          symbol: ['none', 'arrow'],
          lineStyle: {
            color: "#b1b19c",
          },
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisLabel: {
          fontSize: 16,
          color: "#fff",
        },
        boundaryGap: ["20%", "20%"],
      },
      series: [
        {
          type: "custom",
          renderItem: (params, api) => {
            var location = api.coord([api.value(0), api.value(1)]);
            return {
              type: "group",
              children: [
                {
                  type: "CubeLeft",
                  shape: {
                    api,
                    xValue: api.value(0),
                    yValue: api.value(1),
                    x: location[0],
                    y: location[1],
                    xAxisPoint: api.coord([api.value(0), 0]),
                  },
                  style: {
                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                      {
                        offset: 0,
                        color: "#d5ac37",
                      },
                      {
                        offset: 1,
                        color: "#df8244",
                      },
                    ]),
                  },
                },
                {
                  type: "CubeRight",
                  shape: {
                    api,
                    xValue: api.value(0),
                    yValue: api.value(1),
                    x: location[0],
                    y: location[1],
                    xAxisPoint: api.coord([api.value(0), 0]),
                  },
                  style: {
                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                      {
                        offset: 0,
                        color: "#d5ac37",
                      },
                      {
                        offset: 1,
                        color: "#df8244",
                      },
                    ]),
                  },
                },
                {
                  type: "CubeTop",
                  shape: {
                    api,
                    xValue: api.value(0),
                    yValue: api.value(1),
                    x: location[0],
                    y: location[1],
                    xAxisPoint: api.coord([api.value(0), 0]),
                  },
                  style: {
                    fill: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                      {
                        offset: 0,
                        color: "#d5ac37",
                      },
                      {
                        offset: 1,
                        color: "#df8244",
                      },
                    ]),
                  },
                },
              ],
            };
          },
          data: VALUE,
        },
        {
          type: "bar",
          label: {
              show: true,
              position: "top",
              fontSize: 14,
              color: "#fff",
              offset: [2, -25],
            formatter: (params) => {
              return params.data.toFixed(0);
            }
          },
          itemStyle: {
            color: "transparent",
          },
          data: VALUE,
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

export default TopActiveRepos;
