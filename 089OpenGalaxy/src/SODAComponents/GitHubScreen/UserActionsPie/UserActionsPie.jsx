import React from "react";
import ReactEchartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts";
import intl from 'react-intl-universal';

import base64Images from './base64Images.js';
import banner from "./banner.png";

class UserActionsPie extends React.Component {
  render() {
    if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;

    let issueNum = this.props.data.IssuesEvent;
    let issueCommentNum = this.props.data.IssueCommentEvent;
    let PRNum = this.props.data.PullRequestEvent;
    let PRReviewCommentNum = this.props.data.PullRequestReviewCommentEvent;
    let forkNum = this.props.data.ForkEvent;
    let watchNum = this.props.data.WatchEvent;

    var back1 = new Image();
    back1.src = base64Images.bg1;
    var back2 = new Image();
    back2.src = base64Images.bg2;
    var back3 = new Image();
    back3.src = base64Images.bg3;
    var back4 = new Image();
    back4.src = base64Images.bg4;
    var back5 = new Image();
    back5.src = base64Images.bg5;
    var back6 = new Image();
    back6.src = base64Images.bg6;

    const option = {
      // backgroundColor: "#212434",
      title: {
        show: true,
        text: `{imgBg|${intl.get('UserActionsPie_TITLE')}}`,
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
        left: -100,
        top: 50,
        bottom: 10,
        right: 10,
        containLabel: true,
      },
      tooltip: {
        // backgroundColor: "rgba(0,0,0,0.9)",
        trigger: "item",
        formatter: "{b} : {c} ({d}%)",
      },
      // legend: {
      //   top: 20,
      //   left: "center",
      //   itemWidth: 20,
      //   itemHeight: 8,
      //   textStyle: {
      //     color: "#aab2cd",
      //   },
      // },
      polar: {
        center: ["50%", "55%"],
      },
      angleAxis: {
        interval: 1,
        type: "category",
        data: [],
        z: 10,
        axisLine: {
          show: false,
          lineStyle: {
            color: "#0B4A6B",
            width: 1,
            type: "solid",
          },
        },
        axisLabel: {
          interval: 0,
          show: true,
          color: "#0B4A6B",
          margin: 8,
          fontSize: 16,
        },
      },
      radiusAxis: {
        min: 0,
        max: 100,
        interval: 25,
        axisLine: {
          show: false,
          lineStyle: {
            color: "#0B3E5E",
            width: 1,
            type: "solid",
          },
        },
        axisLabel: {
          formatter: "{value} %",
          show: false,
          padding: [0, 0, 20, 0],
          color: "#0B3E5E",
          fontSize: 16,
        },
        splitLine: {
          show: false,
        },
      },
      calculable: true,
      series: [
        {
          stack: "a",
          type: "pie",
          radius: ["0%", "55%"],
          // roseType: "radius",
          // center: ["45%", "55%"],
          zlevel: 10,
          itemStyle: {
            borderRadius: 100,
          },
          startAngle: 10,
          label: {
            normal: {
              // formatter: ["{b|{b}}", "{c|{c}}"].join("\n"),
              formatter: (params) => {
                return [
                  `{b|${params.data.name}}`,
                  `{c|${numFormat(params.data.value, 1)}}`,
                ].join("\n");
              },
              rich: {
                b: {
                  color: "#aab2cd",
                  lineHeight: 20,
                },
                c: {
                  color: "#3bd2fe",
                  fontFamily: "Lato",
                  fontWeight: "100",
                  fontSize: 14,
                  height: 20,
                },
              },
            },
          },
          labelLine: {
            normal: {
              show: true,
              length: 10,
              length2: 45,
              smooth: true,
              lineStyle: {
                width: 2,
              },
            },
            emphasis: {
              show: false,
            },
          },
          data: [
            {
              value: issueNum,
              name: intl.get('UserActionsPie_OPEN_ISSUE'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back1,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
            {
              value: issueCommentNum,
              name: intl.get('UserActionsPie_COMMENT_ISSUE'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back2,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
            {
              value: PRNum,
              name: intl.get('UserActionsPie_OPEN_PR'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back3,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
            {
              value: PRReviewCommentNum,
              name: intl.get('UserActionsPie_COMMENT_PR'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back4,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
            {
              value: forkNum,
              name: intl.get('UserActionsPie_FORK'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back5,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
            {
              value: watchNum,
              name: intl.get('UserActionsPie_WATCH'),
              itemStyle: {
                normal: {
                  opacity: 1,
                  color: {
                    image: back6,
                    repeat: "repeat",
                  },
                  shadowBlur: 20,
                  shadowColor: "rgba(0, 0, 0, .6)",
                  shadowOffsetX: 5,
                  shadowOffsetY: 5,
                },
              },
            },
          ],
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

export default UserActionsPie;
