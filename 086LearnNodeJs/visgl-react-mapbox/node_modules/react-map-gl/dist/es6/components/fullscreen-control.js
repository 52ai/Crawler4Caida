import { document } from '../utils/globals';
import * as PropTypes from 'prop-types';
import * as React from 'react';
import { useEffect, useState, useMemo } from 'react';
import mapboxgl from '../utils/mapboxgl';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
const propTypes = Object.assign({}, mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  container: PropTypes.object,
  label: PropTypes.string
});
const defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  container: null,
  label: 'Toggle fullscreen'
});

function FullscreenControl(props) {
  const {
    context,
    containerRef
  } = useMapControl(props);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showButton, setShowButton] = useState(false);
  const [mapboxFullscreenControl, createMapboxFullscreenControl] = useState(null);
  useEffect(() => {
    const control = new mapboxgl.FullscreenControl();
    createMapboxFullscreenControl(control);
    setShowButton(control._checkFullscreenSupport());

    const onFullscreenChange = () => {
      const nextState = !control._fullscreen;
      control._fullscreen = nextState;
      setIsFullscreen(nextState);
    };

    document.addEventListener(control._fullscreenchange, onFullscreenChange);
    return () => {
      document.removeEventListener(control._fullscreenchange, onFullscreenChange);
    };
  }, []);

  const onClickFullscreen = () => {
    if (mapboxFullscreenControl) {
      mapboxFullscreenControl._container = props.container || context.container;

      mapboxFullscreenControl._onClickFullscreen();
    }
  };

  const style = useMemo(() => ({
    position: 'absolute',
    ...props.style
  }), [props.style]);

  if (!showButton) {
    return null;
  }

  const {
    className,
    label
  } = props;
  const type = isFullscreen ? 'shrink' : 'fullscreen';
  return React.createElement("div", {
    style: style,
    className: className
  }, React.createElement("div", {
    className: "mapboxgl-ctrl mapboxgl-ctrl-group",
    ref: containerRef
  }, React.createElement("button", {
    key: type,
    className: "mapboxgl-ctrl-icon mapboxgl-ctrl-".concat(type),
    type: "button",
    title: label,
    onClick: onClickFullscreen
  }, React.createElement("span", {
    className: "mapboxgl-ctrl-icon",
    "aria-hidden": "true"
  }))));
}

FullscreenControl.propTypes = propTypes;
FullscreenControl.defaultProps = defaultProps;
export default React.memo(FullscreenControl);
//# sourceMappingURL=fullscreen-control.js.map