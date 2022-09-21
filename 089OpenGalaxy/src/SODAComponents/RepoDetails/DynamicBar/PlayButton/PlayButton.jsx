import React from "react";
import './PlayButton.less';

import intl from 'react-intl-universal';

class PlayButton extends React.Component {
  render() {
    if (this.props.hide) return null;
    return (
      <div>
        <button className='play-button' onClick={this.props.play}>
          {intl.get('PLAY_BUTTON')}
        </button>
      </div>
    );
  }
}
export default PlayButton;
