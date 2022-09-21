import React from "react";
import detailModel from "./RepoDetailsStore.js";
import "./RepoDetails.less";

import DynamicBar from "./DynamicBar/DynamicBar.jsx";
import ProjectNetwork from "./ProjectNetwork/ProjectNetwork.jsx";
import ContributorNetwork from "./ContributorNetwork/ContributorNetwork.jsx";

import intl from 'react-intl-universal';

class RepoDetails extends React.Component {
  constructor() {
    super();
  this.state = {
    currentRepoFullname: null,
    // contributorsActivityEvolutionDataUrl: null,
    projectNetworkData: null,
    contributorNetworkData: null,
  };
    this.updateView = this.updateView.bind(this);
  }

  render() {
    if (
      !this.state.currentRepoFullname ||
      // !this.state.contributorsActivityEvolutionDataUrl ||
      !this.state.projectNetworkData ||
      !this.state.contributorNetworkData
    )
      return null;

    return (
      <div>
        {/* <div className="cool-box contributors-activity-evolution-box"> */}
        {/*   <h3>{intl.get('CONTRIBUTOR_ACTIVITY_EVOLUTION')}</h3> */}
        {/*   <DynamicBar */}
        {/*     theme="dark" */}
        {/*     width={600} */}
        {/*     height={600} */}
        {/*     barNumber={20} */}
        {/*     digitNumber={2} */}
        {/*     duration={30} */}
        {/*     dateLabelSize={30} */}
        {/*     dataUrl={this.state.contributorsActivityEvolutionDataUrl} */}
        {/*   /> */}
        {/* </div> */}

        <div className="cool-box two-networks-box">
          <div className="project-network-box">
            <h3>{intl.get('PROJECT_CORRELATION_NETWORK')}</h3>
            <ProjectNetwork
              currentNode={this.state.currentRepoFullname}
              data={this.state.projectNetworkData}
            />
          </div>
          <div className="contributor-network-box">
            <h3>{intl.get('CONTRIBUTOR_CORRELATION_NETWORK')}</h3>
            <ContributorNetwork data={this.state.contributorNetworkData} />
          </div>
        </div>
      </div>
    );
  };

  componentDidMount() {
    detailModel.on("changed", this.updateView);
  };

  componentWillUnmount() {
    detailModel.off("changed", this.updateView);
  };

  updateView() {
    detailModel
      .loadRepodetails()
      .then((data) => {
        this.setState({
          currentRepoFullname: data.currentRepoFullname,
          // contributorsActivityEvolutionDataUrl:
          //   data.contributorsActivityEvolutionDataUrl,
          projectNetworkData: data.projectNetworkData,
          contributorNetworkData: data.contributorNetworkData,
        });
      })
      .catch((message) => {
        // window.alert('未选中结点或该结点的详细数据不存在。')
        console.log(message);
        this.setState({
          currentRepoFullname: null,
          // contributorsActivityEvolutionDataUrl: null,
          projectNetworkData: null,
          contributorNetworkData: null,
        });
      });
  }
}

export default RepoDetails;
