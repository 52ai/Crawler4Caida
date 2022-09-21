import React from "react";
import ReactEchartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts";
import intl from 'react-intl-universal';

import banner from "./banner.png";

// import svg from "./dragon-scales.svg";
// const patternImg = new Image();
// patternImg.src = svg;

class TopLanguages extends React.Component {
  render() {
    if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;
    let data = this.props.data;

    const option = {
      title: {
        show: true,
        text: `{imgBg|${intl.get('TopLanguages_TITLE')}}`,
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
      tooltip: {},
      series: [
        {
          type: "pie",
          radius: "60%",
          selectedMode: "single",
          selectedOffset: 30,
          clockwise: true,
          label: {
            fontSize: 14,
            color: "#00AEE4",
          },
          labelLine: {
            lineStyle: {
              color: "#235894",
            },
          },
          data: data,
          itemStyle: {
            opacity: 1,
            color: '#277AFD',
            // color: {
            //   image: patternImg,
            //   repeat: "repeat",
            // },
            borderWidth: 1,
            borderColor: "white",
          },
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

export default TopLanguages;
