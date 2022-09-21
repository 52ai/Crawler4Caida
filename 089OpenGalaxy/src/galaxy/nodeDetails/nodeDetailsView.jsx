import React from 'react';
import detailModel from './nodeDetailsStore.js';
import specialNodeDetails from './templates/all.js';
import scene from '../store/scene.js';

class detailedNodeView extends React.Component {
  constructor() {
    super();
    this.getNodeDetails = this.getNodeDetails.bind(this);
    this.updateView = this.updateView.bind(this);
  }

  render() {
    var selectedNode = detailModel.getSelectedNode();
    if (!selectedNode) return null;
    var NodeDetails = this.getNodeDetails(selectedNode);

    return (
      <div className='node-details'>
        <NodeDetails model={selectedNode} />
      </div>
    );
  };

  componentDidMount() {
    detailModel.on('changed', this.updateView);
  };

  componentWillUnmount() {
    detailModel.off('changed', this.updateView);
  };

  getNodeDetails(viewModel) {
    var Template = specialNodeDetails[scene.getGraphName()] || specialNodeDetails.default;
    return Template;
  }

  updateView() {
    this.forceUpdate();
  }
}

export default detailedNodeView;
