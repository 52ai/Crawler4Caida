import React from "react";

import "./GitHubScreen.less";
import appEvents from "../../galaxy/service/appEvents.js";
import request from "../../galaxy/service/request.js";

import ReposUsersTotal from "./ReposUsersTotal/ReposUsersTotal.jsx";
import MonthlyActiveReposAndUsers from "./MonthlyActiveReposAndUsers/MonthlyActiveReposAndUsers.jsx";
import UserActionsPie from "./UserActionsPie/UserActionsPie.jsx";
import TopLanguages from "./TopLanguages/TopLanguages.jsx";
import TopActiveRepos from "./TopActiveRepos/TopActiveRepos.jsx";
import ContributorsGeoDistribution from "./ContributorsGeoDistribution/ContributorsGeoDistribution.jsx";
import CompaniesScatter from "./CompaniesScatter/CompaniesScatter.jsx";

// var BASE_URL = "http://192.168.3.16:8081";
var BASE_URL = "https://nzcer.cn:8081";

class GitHubScreen extends React.Component {
  constructor() {
    super();
    this.state = {
      visibility: "hidden", // or "visible", 初始时隐藏
      repos_and_users_monthly_counts: null,
      actions_count: null,
      languages_count: null,
      repo_activities_top20: null,
      repos_and_users_total: null,
      companies_scatter: null,
    };
  }

  componentDidMount() {
    // 开始监听: sceneKeyboardBinding.js中按下BackQuote键就fire了该事件
    appEvents.toggleGitHubScreen.on(() => {
      this.setState({
        visibility: this.state.visibility === "visible" ? "hidden" : "visible",
      });
    });

    // 请求各种数据
    request(BASE_URL + "/repoUserCount", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        repos_and_users_monthly_counts: data,
      });
    });

    request(BASE_URL + "/actionsCount", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        actions_count: data,
      });
    });

    request(BASE_URL + "/languagesCount", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        languages_count: data,
      });
    });

    request(BASE_URL + "/repoActivity", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        repo_activities_top20: data,
      });
    });


    request(BASE_URL + "/totalRepoUserCount", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        repos_and_users_total: data,
      });
    });

    request(BASE_URL + "/totalCompanyRepoActivity", {
      responseType: "json",
    }).then((data) => {
      this.setState({
        companies_scatter: data.scatters,
      });
    });
  }

  componentWillUnmount() {}

  render() {
    return (
      <div
        className="github-screen"
        style={{ zIndex: 999, visibility: this.state.visibility }}
      >
        <div style={{ position: "absolute", left: 100, top: 400 }}>
          <ReposUsersTotal width={1700} height={140} data={this.state.repos_and_users_total} />
        </div>
        <div style={{ position: "absolute", left: 0, top: 0 }}>
          <MonthlyActiveReposAndUsers
            width={500}
            height={400}
            data={this.state.repos_and_users_monthly_counts}
          />
        </div>
        <div style={{ position: "absolute", left: 0, top: 550 }}>
          <TopLanguages
            width={500}
            height={500}
            data={this.state.languages_count}
          />
        </div>

        <div style={{ position: "absolute", left: 560, top: 0 }}>
          <ContributorsGeoDistribution width={800} height={400} />
        </div>
        <div style={{ position: "absolute", left: 560, top: 550 }}>
          <TopActiveRepos
            width={800}
            height={500}
            data={this.state.repo_activities_top20}
          />
        </div>

        <div style={{ position: "absolute", left: 1350, top: 0 }}>
          <UserActionsPie
            width={500}
            height={400}
            data={this.state.actions_count}
          />
        </div>

        <div style={{ position: "absolute", left: 1380, top: 550 }}>
          <CompaniesScatter
            width={500}
            height={500}
            data={this.state.companies_scatter}
            logoBaseUrl={`${BASE_URL}/companies_logos`}
          />
        </div>
      </div>
    );
  }
}

export default GitHubScreen;
