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

g.forEachLinkedNode('hello', function(linkedNode, link){
        console.log("Connected node:", linkedNode.id, linkedNode.data);
        console.dir(link);
}, true);// true, so get only outbound links

var world = g.getNode('world');// return 'word' node
console.log(world.id, world.data)

// waiting to learn

var helloWorldLink = g.getLink('hello', 'world');
console.log(helloWorldLink);

console.log("Before Delete Node:")
g.forEachNode(function(node){
        console.log(node.id, node.data);
});
g.removeNode('space');
console.log("After Delete Node:")
g.forEachNode(function(node){
        console.log(node.id, node.data);
});

console.log("Before Delete Link:")
g.forEachLink(function(link){
        console.dir(link);
});
//Removing link is a bit harder, since method requires actual link object
g.forEachLinkedNode('hello', function(linkedNode, link){
        g.removeLink(link)
});
console.log("After Delete Link:")
g.forEachLink(function(link){
        console.dir(link);
});

g.on('changed', function(changes){
    console.dir(changes); // prints array of change records
});

g.addNode(42);

g.beginUpdate();
for(var i = 0; i < 3; ++i) {
  g.addLink(i, i + 1); // no events are triggered here
}
g.endUpdate(); // this triggers all listeners of 'changed' event

var country = "AS2-UniversityofDelaware-US";
console.log(country.toString().split('-')[2]);
console.log(country.toString().split('-')[2] === "US");