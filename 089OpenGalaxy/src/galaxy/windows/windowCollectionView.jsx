/**
 * Renders collection of windows
 */
import React from 'react';
import NodeListView from './nodeListView.jsx';
import windowCollectionModel from './windowCollectionModel.js';

class windowCollectionView extends React.Component {
  constructor() {
    super();
    this.toWindowView = this.toWindowView.bind(this);
    this.update = this.update.bind(this);
  }
  render() {
    var windows = windowCollectionModel.getWindows();
    if (windows.length === 0) return null;

    return <div>{windows.map(this.toWindowView)}</div>;
  };

  componentDidMount() {
    windowCollectionModel.on('changed', this.update);
  };

  componentWillUnmount() {
    windowCollectionModel.off('changed', this.update);
  };

  toWindowView(windowViewModel, idx) {
    return <NodeListView viewModel={windowViewModel} key={idx} />;
  }

  update() {
    this.forceUpdate();
  }
}

export default windowCollectionView;
