import React from "react";
import ReactEchartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts";

import banner from "./banner.png";

class Template extends React.Component {
  render() {
    if (!this.props.data) return null;

    let xxx = this.props.data.xxx;

    const option = {
      title: {
        show: true,
        text: "{imgBg|Your Title Here}",
        left: "center",
        top: 0,
        textStyle: {
          rich: {
            imgBg: {
              fontSize: 16,
              fontWeight: "bold",
              color: "white",
              backgroundColor: {
                image: banner,
              },
              width: 300,
              height: 50,
            },
          },
        },
      },
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

export default Template;
