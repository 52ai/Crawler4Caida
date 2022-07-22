var graph = require('ngraph.graph')();
graph.addLink(1, 2);

var renderGraph = require('ngraph.pixel');
var renderer = renderGraph(graph, {
  node: createNodeUI
});

function createNodeUI(node) {
  return {
    color: 0xFF00FF,
    size: 20
  };
}