var createGraph = require('ngraph.graph');
var emptyArray = [];
module.exports = toGraph;

function toGraph(allPackages) {
  var graph = createGraph();
  allPackages.forEach(addToGraph);

  return graph;

  function addToGraph(pkg) {
    graph.addNode(pkg.name);
    var dependencies = getPackageDeps(pkg.require);
    for (var i = 0; i < dependencies.length; ++i) {
      if (!graph.hasLink(pkg.name, dependencies[i])) {
        graph.addLink(pkg.name, dependencies[i]);
      }
    }
  }
}

function getPackageDeps(requires) {
  if (!requires) return emptyArray;
  return Object.keys(requires).filter(byPackageNames);
}

function byPackageNames(str) {
  return str && str.indexOf('/') > -1;
}
