import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import { useEffect, useState, useMemo } from 'react';
import * as PropTypes from 'prop-types';
import mapboxgl from '../utils/mapboxgl';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
var propTypes = Object.assign({}, mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  maxWidth: PropTypes.number,
  unit: PropTypes.oneOf(['imperial', 'metric', 'nautical'])
});
var defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  maxWidth: 100,
  unit: 'metric'
});

function ScaleControl(props) {
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var _useState = useState(null),
      _useState2 = _slicedToArray(_useState, 2),
      mapboxScaleControl = _useState2[0],
      createMapboxScaleControl = _useState2[1];

  useEffect(function () {
    if (context.map) {
      var control = new mapboxgl.ScaleControl();
      control._map = context.map;
      control._container = containerRef.current;
      createMapboxScaleControl(control);
    }
  }, [context.map]);

  if (mapboxScaleControl) {
    mapboxScaleControl.options = props;

    mapboxScaleControl._onMove();
  }

  var style = useMemo(function () {
    return _objectSpread({
      position: 'absolute'
    }, props.style);
  }, [props.style]);
  return React.createElement("div", {
    style: style,
    className: props.className
  }, React.createElement("div", {
    ref: containerRef,
    className: "mapboxgl-ctrl mapboxgl-ctrl-scale"
  }));
}

ScaleControl.propTypes = propTypes;
ScaleControl.defaultProps = defaultProps;
export default React.memo(ScaleControl);
//# sourceMappingURL=scale-control.js.map