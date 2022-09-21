import React from "react";
import intl from "react-intl-universal";

import banner from "./banner.png";
import world2020 from "./world-2020.svg";

class ContributorsGeoDistribution extends React.Component {
  render() {
    // if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;

    return (
      <div
        style={{
          width: width,
          height: height,
        }}
      >
        <div
          style={{
            height: 50,
            marginTop: 5,
            marginBottom: 5,
            // 水平、垂直居中文字 ---- 外层设置即可
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              lineHeight: '50px',
              backgroundImage: `url(${banner})`,
              backgroundSize: "100% 100%",
              backgroundRepeat: "no-repeat",
              fontSize: 16,
              fontWeight: "bold",
              color: "white",
              paddingLeft: 30,
              paddingRight: 20,
            }}
          >
              {intl.get("ContributorsGeoDistribution_TITLE")}
          </div>
        </div>
        <img src={world2020} width={width} height={height - 50 - 5 - 5} />
      </div>
    );
  }
}

export default ContributorsGeoDistribution;
