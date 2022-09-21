import React from 'react';
import hoverModel from './store/hover.js';

class hoverInfo extends React.Component {
  constructor() {
    super();
    this.updateView = this.updateView.bind(this);
  }

  hoverTemplate = null;

  render() {
    return this.hoverTemplate;
  };

  componentDidMount() {
    hoverModel.on('changed', this.updateView);
  };

  componentWillUnmount() {
    hoverModel.off('changed', this.updateView);
  };

  updateView(viewTemplate) {
    this.hoverTemplate = viewTemplate;
    this.forceUpdate();
  }
}

export default hoverInfo;
