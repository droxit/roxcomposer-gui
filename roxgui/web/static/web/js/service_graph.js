// Define nodes.
var node_data = [{
		"name": "file_writer",
		"json": {},
		"active": true
	},
	{
		"name": "html_generator",
		"json": {},
		"active": true
	},
	{
		"name": "image_adder",
		"json": {},
		"active": true
	},
];

// Define links between nodes.
var link_data = [{
		"source": "html_generator",
		"target": "image_adder"
	},
	{
		"source": "image_adder",
		"target": "file_writer"
	},
];

// Get D3 graph.
var svg = d3.select("svg");
var width = +svg.attr("width");
var height = +svg.attr("height");

// Add nodes to simulation.
var simulation = d3.forceSimulation().nodes(node_data);

// Create two forces. The first makes sure that every node leaves enough space
// to its neighbours. The second pulls every node to the center of the diagram.
simulation.force("charge_force", d3.forceManyBody()).force("center_force", d3.forceCenter(width / 2, height / 2));

// Create a force concerning each link and add it to simulation.
var link_force = d3.forceLink(link_data).id(function(d) {
	return d.name;
});
simulation.force("links", link_force);

// Draw a circle for each node.
var node = svg.append("g")
	.attr("class", "nodes")
	.selectAll("circle")
	.data(node_data)
	.enter()
	.append("circle")
	.attr("r", 5)
	.attr("fill", "red");

// Draw a line for each link.
var link = svg.append("g")
	.attr("class", "links")
	.selectAll("line")
	.data(link_data)
	.enter()
	.append("line")
	.attr("fill", "red")
	.attr("stroke", "black")
	.attr("stroke-width", 2);

// Start simulation.
simulation.on("tick", tickActions);

function tickActions() {
	// Update graphical location of nodes after each simulation step.
	node
		.attr("cx", function(d) {
			return d.x;
		})
		.attr("cy", function(d) {
			return d.y;
		});
	// Update graphical location of links after each simulation step.
	link
		.attr("x1", function(d) {
			return d.source.x;
		})
		.attr("y1", function(d) {
			return d.source.y;
		})
		.attr("x2", function(d) {
			return d.target.x;
		})
		.attr("y2", function(d) {
			return d.target.y;
		});
}
