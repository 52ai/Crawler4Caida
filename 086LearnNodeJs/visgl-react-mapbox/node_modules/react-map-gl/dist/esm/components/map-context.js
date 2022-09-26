import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import { createContext, useState, useContext } from 'react';
var MapContext = createContext({
  viewport: null,
  map: null,
  container: null,
  onViewportChange: null,
  onViewStateChange: null,
  eventManager: null
});
export var MapContextProvider = MapContext.Provider;

function WrappedProvider(_ref) {
  var value = _ref.value,
      children = _ref.children;

  var _useState = useState(null),
      _useState2 = _slicedToArray(_useState, 2),
      map = _useState2[0],
      setMap = _useState2[1];

  var context = useContext(MapContext);
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
export default MapContext;
//# sourceMappingURL=map-context.js.map