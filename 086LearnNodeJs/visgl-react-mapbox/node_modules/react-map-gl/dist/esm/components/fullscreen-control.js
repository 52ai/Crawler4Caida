import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import { document } from '../utils/globals';
import * as PropTypes from 'prop-types';
import * as React from 'react';
import { useEffect, useState, useMemo } from 'react';
import mapboxgl from '../utils/mapboxgl';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
var propTypes = Object.assign({}, mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  container: PropTypes.object,
  label: PropTypes.string
});
var defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  container: null,
  label: 'Toggle fullscreen'
});

function FullscreenControl(props) {
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var _useState = useState(false),
      _useState2 = _slicedToArray(_useState, 2),
      isFullscreen = _useState2[0],
      setIsFullscreen = _useState2[1];

  var _useState3 = useState(false),
      _useState4 = _slicedToArray(_useState3, 2),
      showButton = _useState4[0],
      setShowButton = _useState4[1];

  var _useState5 = useState(null),
      _useState6 = _slicedToArray(_useState5, 2),
      mapboxFullscreenControl = _useState6[0],
      createMapboxFullscreenControl = _useState6[1];

  useEffect(function () {
    var control = new mapboxgl.FullscreenControl();
    createMapboxFullscreenControl(control);
    setShowButton(control._checkFullscreenSupport());

    var onFullscreenChange = function onFullscreenChange() {
      var nextState = !control._fullscreen;
      control._fullscreen = nextState;
      setIsFullscreen(nextState);
    };

    document.addEventListener(control._fullscreenchange, onFullscreenChange);
    return function () {
      document.removeEventListener(control._fullscreenchange, onFullscreenChange);
    };
  }, []);

  var onClickFullscreen = function onClickFullscreen() {
    if (mapboxFullscreenControl) {
      mapboxFullscreenControl._container = props.container || context.container;

      mapboxFullscreenControl._onClickFullscreen();
    }
  };

  var style = useMemo(function () {
    return _objectSpread({
      position: 'absolute'
    }, props.style);
  }, [props.style]);

  if (!showButton) {
    return null;
  }

  var className = props.className,
      label = props.label;
  var type = isFullscreen ? 'shrink' : 'fullscreen';
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