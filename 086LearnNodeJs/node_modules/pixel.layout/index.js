/**
 * Creates a force based layout that can be switched between 3d and 2d modes
 * Layout is used by ngraph.pixel
 *
 * @param {ngraph.graph} graph instance that needs to be laid out
 * @param {object} options - configures current layout.
 * @returns {ojbect} api to operate with current layout. Only two methods required
 * to exist by ngraph.pixel: `step()` and `getNodePosition()`.
 */
var eventify = require('ngraph.events');
var layout3d = require('ngraph.forcelayout3d');
var layout2d = layout3d.get2dLayout;

module.exports = createLayout;

function createLayout(graph, options) {
  options = options || {};

  /**
   * Should the graph be rendered in 3d space? True by default
   */
  options.is3d = options.is3d === undefined ? true : options.is3d;

  var is3d = options.is3d;
  var layout = is3d ? layout3d(graph, options.physics) : layout2d(graph, options.physics);

  var api = {
    ////////////////////////////////////////////////////////////////////////////
    // The following two methods are required by ngraph.pixel to be implemented
    // by all layout providers
    ////////////////////////////////////////////////////////////////////////////

    /**
     * Called by `ngraph.pixel` to perform one step. Required to be provided by
     * all layout interfaces.
     */
    step: layout.step,

    /**
     * Gets position of a given node by its identifier. Required.
     *
     * @param {string} nodeId identifier of a node in question.
     * @returns {object} {x: number, y: number, z: number} coordinates of a node.
     */
    getNodePosition: layout.getNodePosition,

    ////////////////////////////////////////////////////////////////////////////
    // Methods below are not required by ngraph.pixel, and are specific to the
    // current layout implementation
    ////////////////////////////////////////////////////////////////////////////

    /**
     * Sets position for a given node by its identifier.
     *
     * @param {string} nodeId identifier of a node that we want to modify
     * @param {number} x coordinate of a node
     * @param {number} y coordinate of a node
     * @param {number} z coordinate of a node
     */
    setNodePosition: layout.setNodePosition,

    /**
     * Toggle rendering mode between 2d and 3d.
     *
     * @param {boolean+} newMode if set to true, the renderer will switch to 3d
     * rendering mode. If set to false, the renderer will switch to 2d mode.
     * Finally if this argument is not defined, then current rendering mode is
     * returned.
     */
    is3d: mode3d,

    /**
     * Gets force based simulator of the current layout
     */
    simulator: layout.simulator,

    /**
     * Toggle node pinning. If node is pinned the layout algorithm is not allowed
     * to change its position.
     *
     * @param {string} nodeId identifier of a node to work with;
     * @param {boolean+} isPinned if specified then the `nodeId` pinning attribute
     * is set to the to the value of this argument; Otherwise this method returns
     * current pinning mode of the node.
     */
    pinNode: pinNode
  };

  eventify(api);

  return api;

  function mode3d(newMode) {
    if (newMode === undefined) {
      return is3d;
    }
    if (newMode !== is3d) {
      toggleLayout();
    }
    return api;
  }

  function toggleLayout() {
    var idx = 0;
    var oldLayout = layout;
    layout.dispose();
    is3d = !is3d;
    var physics = copyPhysicsSettings(layout.simulator);

    if (is3d) {
      layout = layout3d(graph, physics);
    } else {
      layout = layout2d(graph, physics);
    }
    graph.forEachNode(initLayout);
    api.step = layout.step;
    api.setNodePosition = layout.setNodePosition;
    api.getNodePosition = layout.getNodePosition;
    api.simulator = layout.simulator;

    api.fire('reset');

    function initLayout(node) {
      var pos = oldLayout.getNodePosition(node.id);
      // we need to bump 3d positions, so that forces are disturbed:
      if (is3d) pos.z = (idx % 2 === 0) ? -1 : 1;
      else pos.z = 0;
      layout.setNodePosition(node.id, pos.x, pos.y, pos.z);
      idx += 1;
    }
  }

  function pinNode(nodeId, isPinned) {
    var node = graph.getNode(nodeId);
    if (!node) throw new Error('Could not find node in the graph. Node Id: ' + nodeId);
    if (isPinned === undefined) {
      return layout.isNodePinned(node);
    }
    layout.pinNode(node, isPinned);
  }

  function copyPhysicsSettings(simulator) {
    return {
      springLength: simulator.springLength(),
      springCoeff: simulator.springCoeff(),
      gravity: simulator.gravity(),
      theta: simulator.theta(),
      dragCoeff: simulator.dragCoeff(),
      timeStep: simulator.timeStep()
    };
  }
}
