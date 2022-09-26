"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var _slicedToArray2 = _interopRequireDefault(require("@babel/runtime/helpers/slicedToArray"));

var _globals = require("../utils/globals");

var PropTypes = _interopRequireWildcard(require("prop-types"));

var React = _interopRequireWildcard(require("react"));

var _mapboxgl = _interopRequireDefault(require("../utils/mapboxgl"));

var _useMapControl2 = _interopRequireWildcard(require("./use-map-control"));

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var propTypes = Object.assign({}, _useMapControl2.mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  container: PropTypes.object,
  label: PropTypes.string
});
var defaultProps = Object.assign({}, _useMapControl2.mapControlDefaultProps, {
  className: '',
  container: null,
  label: 'Toggle fullscreen'
});

function FullscreenControl(props) {
  var _useMapControl = (0, _useMapControl2["default"])(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var _useState = (0, React.useState)(false),
      _useState2 = (0, _slicedToArray2["default"])(_useState, 2),
      isFullscreen = _useState2[0],
      setIsFullscreen = _useState2[1];

  var _useState3 = (0, React.useState)(false),
      _useState4 = (0, _slicedToArray2["default"])(_useState3, 2),
      showButton = _useState4[0],
      setShowButton = _useState4[1];

  var _useState5 = (0, React.useState)(null),
      _useState6 = (0, _slicedToArray2["default"])(_useState5, 2),
      mapboxFullscreenControl = _useState6[0],
      createMapboxFullscreenControl = _useState6[1];

  (0, React.useEffect)(function () {
    var control = new _mapboxgl["default"].FullscreenControl();
    createMapboxFullscreenControl(control);
    setShowButton(control._checkFullscreenSupport());

    var onFullscreenChange = function onFullscreenChange() {
      var nextState = !control._fullscreen;
      control._fullscreen = nextState;
      setIsFullscreen(nextState);
    };

    _globals.document.addEventListener(control._fullscreenchange, onFullscreenChange);

    return function () {
      _globals.document.removeEventListener(control._fullscreenchange, onFullscreenChange);
    };
  }, []);

  var onClickFullscreen = function onClickFullscreen() {
    if (mapboxFullscreenControl) {
      mapboxFullscreenControl._container = props.container || context.container;

      mapboxFullscreenControl._onClickFullscreen();
    }
  };

  var style = (0, React.useMemo)(function () {
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

var _default = React.memo(FullscreenControl);

exports["default"] = _default;
//# sourceMappingURL=fullscreen-control.js.map