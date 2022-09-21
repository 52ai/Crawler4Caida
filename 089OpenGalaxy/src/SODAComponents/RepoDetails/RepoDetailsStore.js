import appEvents from "../../galaxy/service/appEvents.js";
import eventify from "ngraph.events";
import scene from "../../galaxy/store/scene.js";
import request from "../../galaxy/service/request.js";

export default RepoDetailsStore();

function RepoDetailsStore() {
  var api = {
    loadRepodetails,
  };

  var currentNodeId;
  appEvents.selectNode.on(updateDetails);

  eventify(api);

  return api;

  function updateDetails(nodeId) {
    currentNodeId = nodeId;
    api.fire("changed");
  }

  async function loadRepodetails() {
    if (currentNodeId === undefined) return;

    let currentRepoFullname = scene.getNodeInfo(currentNodeId).name;

//     let contributorsActivityEvolutionDataUrl = `https://hypertrons-oss.x-lab.info/opengalaxy-mock-data/contributors-activity-evolution/data_${
//       currentNodeId % 8
//     }.csv`;

    let projectNetworkDataUrl = `https://open-galaxy-backend.x-lab.info:8443/repo/repo_network/${currentRepoFullname}`;
    let projectNetworkData = await request(projectNetworkDataUrl, {
      responseType: "json",
    });
    if (projectNetworkData.hasOwnProperty("error")) {
      throw(`"${currentRepoFullname}": ${projectNetworkData.error}`);
    }

    let contributorNetworkDataUrl = `https://open-galaxy-backend.x-lab.info:8443/repo/developer_network/${currentRepoFullname}`;
    let contributorNetworkData = await request(contributorNetworkDataUrl, {
      responseType: "json",
    });
    if (contributorNetworkData.hasOwnProperty("error")) {
      throw(`"${currentRepoFullname}": ${contributorNetworkData.error}`);
    }

    return {
      currentRepoFullname,
      // contributorsActivityEvolutionDataUrl,
      projectNetworkData,
      contributorNetworkData,
    };
  }
}
