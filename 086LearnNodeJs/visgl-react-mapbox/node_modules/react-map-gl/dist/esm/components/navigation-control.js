import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import { useMemo } from 'react';
import * as PropTypes from 'prop-types';
import MapState from '../utils/map-state';
import { LINEAR_TRANSITION_PROPS } from '../utils/map-controller';
import { compareVersions } from '../utils/version';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';

var noop = function noop() {};

var propTypes = Object.assign({}, mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  onViewStateChange: PropTypes.func,
  onViewportChange: PropTypes.func,
  showCompass: PropTypes.bool,
  showZoom: PropTypes.bool,
  zoomInLabel: PropTypes.string,
  zoomOutLabel: PropTypes.string,
  compassLabel: PropTypes.string
});
var defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  showCompass: true,
  showZoom: true,
  zoomInLabel: 'Zoom In',
  zoomOutLabel: 'Zoom Out',
  compassLabel: 'Reset North'
});
var VERSION_LEGACY = 1;
var VERSION_1_6 = 2;

function getUIVersion(mapboxVersion) {
  return compareVersions(mapboxVersion, '1.6.0') >= 0 ? VERSION_1_6 : VERSION_LEGACY;
}

function updateViewport(context, props, opts) {
  var viewport = context.viewport;
  var mapState = new MapState(Object.assign({}, viewport, opts));
  var viewState = Object.assign({}, mapState.getViewportProps(), LINEAR_TRANSITION_PROPS);
  var onViewportChange = props.onViewportChange || context.onViewportChange || noop;
  var onViewStateChange = props.onViewStateChange || context.onViewStateChange || noop;
  onViewStateChange({
    viewState: viewState
  });
  onViewportChange(viewState);
}

function renderButton(type, label, callback, children) {
  return React.createElement("button", {
    key: type,
    className: "mapboxgl-ctrl-icon mapboxgl-ctrl-".concat(type),
    type: "button",
    title: label,
    onClick: callback
  }, children || React.createElement("span", {
    className: "mapboxgl-ctrl-icon",
    "aria-hidden": "true"
  }));
}

function renderCompass(context) {
  var uiVersion = useMemo(function () {
    return context.map ? getUIVersion(context.map.version) : VERSION_1_6;
  }, [context.map]);
  var bearing = context.viewport.bearing;
  var style = {
    transform: "rotate(".concat(-bearing, "deg)")
  };
  return uiVersion === VERSION_1_6 ? React.createElement("span", {
    className: "mapboxgl-ctrl-icon",
    "aria-hidden": "true",
    style: style
  }) : React.createElement("span", {
    className: "mapboxgl-ctrl-compass-arrow",
    style: style
  });
}

function NavigationControl(props) {
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var onZoomIn = function onZoomIn() {
    updateViewport(context, props, {
      zoom: context.viewport.zoom + 1
    });
  };

  var onZoomOut = function onZoomOut() {
    updateViewport(context, props, {
      zoom: context.viewport.zoom - 1
    });
  };

  var onResetNorth = function onResetNorth() {
    updateViewport(context, props, {
      bearing: 0,
      pitch: 0
    });
  };

  var className = props.className,
      showCompass = props.showCompass,
      showZoom = props.showZoom,
      zoomInLabel = props.zoomInLabel,
      zoomOutLabel = props.zoomOutLabel,
      compassLabel = props.compassLabel;
  var style = useMemo(function () {
    return _objectSpread({
      position: 'absolute'
    }, props.style);
  }, [props.style]);
  return React.createElement("div", {
    style: style,
    className: className
  }, React.createElement("div", {
    className: "mapboxgl-ctrl mapboxgl-ctrl-group",
    ref: containerRef
  }, showZoom && renderButton('zoom-in', zoomInLabel, onZoomIn), showZoom && renderButton('zoom-out', zoomOutLabel, onZoomOut), showCompass && renderButton('compass', compassLabel, onResetNorth, renderCompass(context))));
}

NavigationControl.propTypes = propTypes;
NavigationControl.defaultProps = defaultProps;
export default React.memo(NavigationControl);
//# sourceMappingURL=navigation-control.js.map