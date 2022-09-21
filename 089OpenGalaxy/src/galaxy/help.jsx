/**
 * This component shows basic navigation help. The idea is to show it only
 * first time when user opens. All subsequent page opening should not trigger
 * help screen.
 *
 * The only possible way to show help again is by triggerign "show help"
 * action, which is currently bound to mouse wheel event
 */
import React from 'react';
import appEvents from './service/appEvents.js';
import Key from './utils/key.js';
import intl from 'react-intl-universal';


var helpWasShown = false;

class help extends React.Component {
  constructor() {
    super();
    this.showHelpIfNeeded = this.showHelpIfNeeded.bind(this);
    this.toggleHelp = this.toggleHelp.bind(this);
    this.resetHelp = this.resetHelp.bind(this);
    this.handlekey = this.handlekey.bind(this);
    this.handlewheel = this.handlewheel.bind(this);
    this.listenToKeys = this.listenToKeys.bind(this);
    this.listenToWheel = this.listenToWheel.bind(this);
    this.releaseKeyListener = this.releaseKeyListener.bind(this);
    this.releaseWheel = this.releaseWheel.bind(this);
  }
  
  graphDownloaded = false;

  render() {
    if (window.orientation !== undefined) {
      // no need to show help on orientation enabled devices
      return null;
    }

    if (helpWasShown) {
      // no need to annoy people
      return null;
    }

    if (!this.graphDownloaded) {
      // Show help only after all is downloaded
      return null;
    }

    return (
      <div className="navigation-help">
        <h3>{intl.get("HELP_TITLE")}</h3>
        <table>
          <tbody>
            <tr>
              <td colSpan="2">
                <code className="important-key">
                  {intl.get("HELP_MOUSE_WHEEL")}
                </code>
              </td>
              <td colSpan="2">{intl.get("HELP_SHOW_GUIDE")}</td>
            </tr>
            <tr className="spacer-row">
              <td colSpan="2">
                <code className="important-key">
                  {intl.get("HELP_ANY_KEY")}
                </code>
              </td>
              <td colSpan="2">{intl.get("HELP_HIDE_GUIDE")}</td>
            </tr>
            <tr>
              <td>
                <code>W</code>
              </td>
              <td>{intl.get("HELP_MOVE_FORWARD")}</td>
              <td>
                <code>Up</code>
              </td>
              <td>{intl.get("HELP_ROTATE_UP")}</td>
            </tr>
            <tr>
              <td>
                <code>S</code>
              </td>
              <td>{intl.get("HELP_MOVE_BACKWARD")}</td>
              <td>
                <code>Down</code>
              </td>
              <td>{intl.get("HELP_ROTATE_DOWN")}</td>
            </tr>
            <tr>
              <td>
                <code>A</code>
              </td>
              <td>{intl.get("HELP_MOVE_LEFT")}</td>
              <td>
                <code>Left</code>
              </td>
              <td>{intl.get("HELP_ROTATE_LEFT")}</td>
            </tr>
            <tr>
              <td>
                <code>D</code>
              </td>
              <td>{intl.get("HELP_MOVE_RIGHT")}</td>
              <td>
                <code>Right</code>
              </td>
              <td>{intl.get("HELP_ROTATE_RIGHT")}</td>
            </tr>
            <tr>
              <td>
                <code>Q</code>
              </td>
              <td>{intl.get("HELP_ROLL_RIGHT")}</td>
              <td>
                <code>R</code>
              </td>
              <td>{intl.get("HELP_FLY_UP")}</td>
            </tr>
            <tr>
              <td>
                <code>E</code>
              </td>
              <td>{intl.get("HELP_ROLL_LEFT")}</td>
              <td>
                <code>F</code>
              </td>
              <td>{intl.get("HELP_FLY_DOWN")}</td>
            </tr>
            <tr>
              <td>
                <code>shift</code>
              </td>
              <td>{intl.get("HELP_MOVE_FASTER")}</td>
              <td>
                <code>Space</code>
              </td>
              <td>{intl.get("HELP_TOGGLE_STEERING")}</td>
            </tr>
            <tr>
              <td>
                <code>L</code>
              </td>
              <td>{intl.get("HELP_TOGGLE_LINK")}</td>
              <td>
                <code>`({intl.get("HELP_BACKQUOTE")})</code>
              </td>
              <td>{intl.get("HELP_TOGGLE_DATA_SCREEN")}</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
    };

  componentDidMount() {
    if (window.orientation !== undefined) return;
    appEvents.graphDownloaded.on(this.showHelpIfNeeded);
    appEvents.downloadGraphRequested.on(this.resetHelp);
    appEvents.toggleHelp.on(this.toggleHelp);

    this.listenToKeys();
    this.listenToWheel();
  }

  componentWillUnmount() {
    if (window.orientation !== undefined) return;
    appEvents.graphDownloaded.off(this.showHelpIfNeeded);
    appEvents.downloadGraphRequested.off(this.resetHelp);
    appEvents.toggleHelp.off(this.toggleHelp);

    this.releaseKeyListener();
    this.releaseWheel();
  }

  showHelpIfNeeded() {
    if (helpWasShown) return;
    this.graphDownloaded = true;

    this.forceUpdate();
  }

  toggleHelp() {
    helpWasShown = !helpWasShown;
    this.forceUpdate();
  }

  resetHelp() {
    this.graphDownloaded = false;
    this.forceUpdate();
  }

  handlekey(e) {
    if (Key.isModifier(e)) {
      // ignore modifiers
      return;
    }
    var needsUpdate = !helpWasShown;
    helpWasShown = true;

    if (needsUpdate) {
      this.forceUpdate();
    }
  }

  handlewheel(e) {
    // only show when used on scene
    if (e.target && e.target.nodeName === 'CANVAS') {
      helpWasShown = false;
      this.forceUpdate();
      appEvents.focusScene.fire();
    }
  }

  listenToKeys() {
    document.body.addEventListener('keydown', this.handlekey);
  }

  listenToWheel() {
    document.body.addEventListener('wheel', this.handlewheel, true);
  }

  releaseKeyListener() {
    document.body.removeEventListener('keydown', this.handlekey, true);
  }

  releaseWheel() {
    document.body.removeEventListener('wheel', this.handlewheel, true);
  }
}

export default help;
