"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = exports.MapContextProvider = void 0;

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var _slicedToArray2 = _interopRequireDefault(require("@babel/runtime/helpers/slicedToArray"));

var React = _interopRequireWildcard(require("react"));

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

var MapContext = (0, React.createContext)({
  viewport: null,
  map: null,
  container: null,
  onViewportChange: null,
  onViewStateChange: null,
  eventManager: null
});
var MapContextProvider = MapContext.Provider;
exports.MapContextProvider = MapContextProvider;

function WrappedProvider(_ref) {
  var value = _ref.value,
      children = _ref.children;

  var _useState = (0, React.useState)(null),
      _useState2 = (0, _slicedToArray2["default"])(_useState, 2),
      map = _useState2[0],
      setMap = _useState2[1];

  var context = (0, React.useContext)(MapContext);
  value = _objectSpread(_objectSpread({
    setMap: setMap
  }, context), {}, {
    map: context && context.map || map
  }, value);
  return React.createElement(MapContextProvider, {
    value: value
  }, children);
}

MapContext.Provider = WrappedProvider;
var _default = MapContext;
exports["default"] = _default;
//# sourceMappingURL=map-context.js.map