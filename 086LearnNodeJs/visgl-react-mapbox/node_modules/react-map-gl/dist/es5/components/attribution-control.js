"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var _slicedToArray2 = _interopRequireDefault(require("@babel/runtime/helpers/slicedToArray"));

var React = _interopRequireWildcard(require("react"));

var PropTypes = _interopRequireWildcard(require("prop-types"));

var _mapboxgl = _interopRequireDefault(require("../utils/mapboxgl"));

var _useMapControl2 = _interopRequireWildcard(require("./use-map-control"));

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var propTypes = Object.assign({}, _useMapControl2.mapControlPropTypes, {
  toggleLabel: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.object,
  compact: PropTypes.bool,
  customAttribution: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)])
});
var defaultProps = Object.assign({}, _useMapControl2.mapControlDefaultProps, {
  className: '',
  toggleLabel: 'Toggle Attribution'
});

function setupAttributioncontrol(opts, map, container, attributionContainer) {
  var control = new _mapboxgl["default"].AttributionControl(opts);
  control._map = map;
  control._container = container;
  control._innerContainer = attributionContainer;

  control._updateAttributions();

  control._updateEditLink();

  map.on('styledata', control._updateData);
  map.on('sourcedata', control._updateData);
  return control;
}

function removeAttributionControl(control) {
  control._map.off('styledata', control._updateData);

  control._map.off('sourcedata', control._updateData);
}

function AttributionControl(props) {
  var _useMapControl = (0, _useMapControl2["default"])(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var innerContainerRef = (0, React.useRef)(null);

  var _useState = (0, React.useState)(false),
      _useState2 = (0, _slicedToArray2["default"])(_useState, 2),
      showCompact = _useState2[0],
      setShowCompact = _useState2[1];

  (0, React.useEffect)(function () {
    var control;

    if (context.map) {
      control = setupAttributioncontrol({
        customAttribution: props.customAttribution
      }, context.map, containerRef.current, innerContainerRef.current);
    }

    return function () {
      return control && removeAttributionControl(control);
    };
  }, [context.map]);
  var compact = props.compact === undefined ? context.viewport.width <= 640 : props.compact;
  (0, React.useEffect)(function () {
    if (!compact && showCompact) {
      setShowCompact(false);
    }
  }, [compact]);
  var toggleAttribution = (0, React.useCallback)(function () {
    return setShowCompact(function (value) {
      return !value;
    });
  }, []);
  var style = (0, React.useMemo)(function () {
    return _objectSpread({
      position: 'absolute'
    }, props.style);
  }, [props.style]);
  return React.createElement("div", {
    style: style,
    className: props.className
  }, React.createElement("div", {
    ref: containerRef,
    "aria-pressed": showCompact,
    className: "mapboxgl-ctrl mapboxgl-ctrl-attrib ".concat(compact ? 'mapboxgl-compact' : '', " ").concat(showCompact ? 'mapboxgl-compact-show' : '')
  }, React.createElement("button", {
    type: "button",
    className: "mapboxgl-ctrl-attrib-button",
    title: props.toggleLabel,
    onClick: toggleAttribution
  }), React.createElement("div", {
    ref: innerContainerRef,
    className: "mapboxgl-ctrl-attrib-inner",
    role: "list"
  })));
}

AttributionControl.propTypes = propTypes;
AttributionControl.defaultProps = defaultProps;

var _default = React.memo(AttributionControl);

exports["default"] = _default;
//# sourceMappingURL=attribution-control.js.map