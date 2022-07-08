var createGraph = require('ngraph.graph');
var g = createGraph();

g.addNode('hello');
g.addNode('world');

g.addLink('space', 'bar');

//Only a link between 'hello' and 'world' is created. No new Nodes.
g.addLink('hello', 'world');
g.addLink('china', 'hello');

//Node 'world' is associated with a string object 'custom data'
g.addNode('world', 'custom data');

//You can associate arbitrary object objects with Node
g.addNode('server', {
    status:'on',
    ip:'127.0.0.1'
});

//to get date back use 'data' property of node
var server = g.getNode('server');
console.log(server.data);//prints associate object

// A link between nodes '1' and '2' is now associated with object 'x'
g.addLink(1, 2, 'x');
g.addLink(2, 3, 'y');

g.forEachNode(function(node){
        console.log(node.id, node.data);
});

g.forEachLink(function(link){
        console.dir(link);
});

g.forEachLinkedNode('hello', function(linkedNode, link){
        console.log("Connected node:", linkedNode.id, linkedNode.data);
        console.dir(link);
}, true);// true, so get only outbound links

var world = g.getNode('world');// return 'word' node
console.log(world.id, world.data)

// waiting to learn
