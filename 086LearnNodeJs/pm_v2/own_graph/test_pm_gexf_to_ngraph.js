var fs = require('fs');
var gexf = require('ngraph.gexf');
var graph = gexf.load(fs.readFileSync('test_pm.gexf', 'utf-8'));

var dir_str = './pm-data-server/my-graph/v2000';

graph.forEachNode(function(node){
        console.log(node.id);
});


//graph.forEachLink(function(link){
//        console.dir(link);
//});

//var createWhisper = require('ngraph.cw');
//
//// Graph is intance of ngraph.graph
//var whisper = createWhisper(graph);
//
//var requiredChangeRate = 0; // 0 is complete convergence
//while (whisper.getChangeRate() > requiredChangeRate) {
//  whisper.step();
//}

//graph.forEachNode(function(node){
//        console.log(node.id, node.data);
//});
//
//graph.forEachLink(function(link){
//        console.dir(link);
//});

//graph.forEachNode(printClass);
//
//function printClass(node) {
//  console.log(node.id + ' belongs to ' + whisper.getClass(node.id));
//}


var createLayout = require('ngraph.offline.layout');
var layout = createLayout(graph,{
  iterations: 2100, // Run `100` iterations only
  saveEach: 1000, // Save each `10th` iteration
  outDir: dir_str, // Save results into `./myFolder`
  layout: require('ngraph.forcelayout3d') // use custom layouter
});

var overwrite = false;
layout.run(overwrite);

var save = require('ngraph.tobinary');
save(graph, {
  outDir: dir_str, // folder where to save results. '.' by default
  labels: 'labels.json', // name of the labels file. labels.json by default
  meta: 'meta.json', // name of the file with meta information. meta.json by default
  links: 'links.bin' // file name for links array. links.bin by default
});
