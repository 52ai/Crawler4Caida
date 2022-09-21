import React from 'react';
import scene from './store/scene.js';

class loadingIndicator extends React.Component {
  constructor() {
    super();
    this.loadingMessage = '';
    this.updateLoadingIndicator = this.updateLoadingIndicator.bind(this);
  }

  render() {
    return scene.isLoading() ?
        <div className='label loading'>{this.loadingMessage}</div> :
        null;
  };

  componentDidMount() {
    scene.on('loadProgress', this.updateLoadingIndicator);
  };

  componentWillUnmount () {
    scene.off('loadProgress', this.updateLoadingIndicator);
  };

  updateLoadingIndicator(progress) {
    this.loadingMessage = `${progress.message} - ${progress.completed}`;
    this.forceUpdate();
  }
}

export default loadingIndicator;
