import React from "react";
import * as echarts from "echarts";

const NODE_SIZE = [10, 30];
const NODE_COLOR = ["#0E4429", "#006D32", "#26A641", "#39D353"];
const THRESHOLD = [10, 100, 1000];

let option = {
  tooltip: {},
  animation: true,
  animationDuration: 2000,
  series: [
    {
      type: "graph",
      layout: "force",
      nodes: null,
      edges: null,
      roam: true,
      label: {
        color: "white",
        fontSize: 14,
      },
      force: {
        initLayout: "circular",
        repulsion: 50,
        edgeLength: [1, 100],
        layoutAnimation: false,
      },
      lineStyle: {
        curveness: 0.3,
        opacity: 0.7,
      },
      emphasis: {
        focus: "adjacency",
        label: {
          position: "top",
          show: true,
        },
      },
    },
  ],
};

class ContributorNetwork extends React.Component {
  constructor() {
    super();
    this.echartsInstance = null;
  }

  componentDidMount() {
    this.echartsInstance = echarts.init(
      document.getElementById("contributor-network")
    );

    this.echartsInstance.on("click", (e) => {
      const url = "https://github.com/" + e.data.id;
      window.open(url, "_blank");
    });

    let graphData = generateGraphData(this.props.data);

    option.series[0].nodes = graphData.nodes;
    option.series[0].edges = graphData.edges;

    this.echartsInstance.setOption(option);
  }

  componentWillUnmount() {
    this.echartsInstance.dispose();
  }

  componentDidUpdate() {
    let graphData = generateGraphData(this.props.data);

    option.series[0].nodes = graphData.nodes;
    option.series[0].edges = graphData.edges;

    this.echartsInstance.setOption(option);
  }

  render() {
    if (!this.props.data) return null;

    return (
      <div>
        <canvas width={320} height={360} id="contributor-network" />
      </div>
    );
  }
}

const generateGraphData = (data) => {
  const generateNodes = (nodes) => {
    const minMax = getMinMax(nodes);
    return nodes.map((n) => {
      return {
        id: n.name,
        name: n.name,
        value: n.value,
        symbol: `image://https://avatars.githubusercontent.com/${n.name}?s=128&v=4`,
        symbolSize: linearMap(n.value, minMax, NODE_SIZE),
        itemStyle: {
          color: getColorMap(n.value),
        },
      };
    });
  };
  const generateEdges = (edges) => {
    return edges.map((e) => {
      return {
        source: e.source,
        target: e.target,
        value: e.weight,
      };
    });
  };
  return {
    nodes: generateNodes(data.nodes),
    edges: generateEdges(data.edges),
  };
};

function getMinMax(data) {
  const newArr = data.map((item) => {
    return item.value;
  });
  return [Math.min(...newArr), Math.max(...newArr)];
}
function linearMap(val, domain, range) {
  const d0 = domain[0];
  const d1 = domain[1];
  const r0 = range[0];
  const r1 = range[1];

  const subDomain = d1 - d0;
  const subRange = r1 - r0;

  if (subDomain === 0) {
    return subRange === 0 ? r0 : (r0 + r1) / 2;
  }
  if (subDomain > 0) {
    if (val <= d0) {
      return r0;
    } else if (val >= d1) {
      return r1;
    }
  } else {
    if (val >= d0) {
      return r0;
    } else if (val <= d1) {
      return r1;
    }
  }

  return ((val - d0) / subDomain) * subRange + r0;
}

const getColorMap = (value) => {
  const length = Math.min(THRESHOLD.length, NODE_COLOR.length - 1);
  let i = 0;
  for (; i < length; i++) {
    if (value < THRESHOLD[i]) {
      return NODE_COLOR[i];
    }
  }
  return NODE_COLOR[i];
};

export default ContributorNetwork;
