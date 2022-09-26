"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var React = _interopRequireWildcard(require("react"));

var PropTypes = _interopRequireWildcard(require("prop-types"));

var _mapState = _interopRequireDefault(require("../utils/map-state"));

var _mapController = require("../utils/map-controller");

var _version = require("../utils/version");

var _useMapControl2 = _interopRequireWildcard(require("./use-map-control"));

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var noop = function noop() {};

var propTypes = Object.assign({}, _useMapControl2.mapControlPropTypes, {
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
var defaultProps = Object.assign({}, _useMapControl2.mapControlDefaultProps, {
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
  return (0, _version.compareVersions)(mapboxVersion, '1.6.0') >= 0 ? VERSION_1_6 : VERSION_LEGACY;
}

function updateViewport(context, props, opts) {
  var viewport = context.viewport;
  var mapState = new _mapState["default"](Object.assign({}, viewport, opts));
  var viewState = Object.assign({}, mapState.getViewportProps(), _mapController.LINEAR_TRANSITION_PROPS);
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
  var uiVersion = (0, React.useMemo)(function () {
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
  var _useMapControl = (0, _useMapControl2["default"])(props),
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
  var style = (0, React.useMemo)(function () {
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

var _default = React.memo(NavigationControl);

exports["default"] = _default;
//# sourceMappingURL=navigation-control.js.map