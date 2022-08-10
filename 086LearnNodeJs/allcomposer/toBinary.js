var graph = require('./lib/loadGraph.js')(process.argv[2] || 'composer_packages.json');

var save = require('ngraph.tobinary');
save(graph, { outDir: './data' });

console.log('Done.');
console.log('Copy `links.bin`, `labels.bin` and positions.bin into vis folder');
