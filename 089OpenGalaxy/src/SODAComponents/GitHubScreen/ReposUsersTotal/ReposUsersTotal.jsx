import React from "react";
import githubLogo from "./github-logo.svg";
import intl from 'react-intl-universal';

class ReposUsersTotal extends React.Component {
  render() {
    if (!this.props.data) return null;

    let width = this.props.width;
    let height = this.props.height;
    let reposTotal = this.props.data.repos_total;
    let usersTotal = this.props.data.users_total;

    return (
      <div
        style={{
          borderBottom: "1px solid rgb(255,255,255,0.8)",
          borderTop: "1px solid rgb(255,255,255,0.8)",
          width: width,
          height: height,
          position: "absolute",
        }}
      >
        <div style={{ position: "absolute", left: 100, top: 5 }}>
          <div
            style={{
              height: height-10,
              fontWeight: "normal",
              fontSize: 75,
              opacity: 1,
              color: "white",
              lineHeight: `${height-10}px`,
            }}
          >
            {intl.get('ReposUsersTotal_REPOS')} {toThousands(reposTotal)}
          </div>
        </div>

        <div style={{ position: "absolute", left: 820, top: 10 }}>
          <img height={120} width={120} src={githubLogo} />
        </div>

        <div style={{ position: "absolute", right: 120, top: 5 }}>
          <div
            style={{
              height: height-10,
              fontWeight: "normal",
              fontSize: 75,
              opacity: 1,
              color: "white",
              lineHeight: `${height-10}px`,
            }}
          >
            {intl.get('ReposUsersTotal_USERS')} {toThousands(usersTotal)}
          </div>
        </div>
      </div>
    );
  }
}

//数字格式化, 每3位加逗号
function toThousands(num) {
  var result = [],
    counter = 0;
  num = (num || 0).toString().split("");
  for (var i = num.length - 1; i >= 0; i--) {
    counter++;
    result.unshift(num[i]);
    if (!(counter % 3) && i != 0) {
      result.unshift(",");
    }
  }
  return result.join("");
}

export default ReposUsersTotal;
