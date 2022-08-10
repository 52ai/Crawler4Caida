var fs = require('fs');
var getGraph = require('./convertToGraph.js');

module.exports = loadGraph;

function loadGraph(inputFileName) {
  var input = JSON.parse(fs.readFileSync(inputFileName, 'utf8'));
  return getGraph(input);
}
