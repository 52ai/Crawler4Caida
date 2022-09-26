import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import { useEffect, useCallback, useState, useRef, useMemo } from 'react';
import * as PropTypes from 'prop-types';
import mapboxgl from '../utils/mapboxgl';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
var propTypes = Object.assign({}, mapControlPropTypes, {
  toggleLabel: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.object,
  compact: PropTypes.bool,
  customAttribution: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)])
});
var defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  toggleLabel: 'Toggle Attribution'
});

function setupAttributioncontrol(opts, map, container, attributionContainer) {
  var control = new mapboxgl.AttributionControl(opts);
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
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var innerContainerRef = useRef(null);

  var _useState = useState(false),
      _useState2 = _slicedToArray(_useState, 2),
      showCompact = _useState2[0],
      setShowCompact = _useState2[1];

  useEffect(function () {
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
  useEffect(function () {
    if (!compact && showCompact) {
      setShowCompact(false);
    }
  }, [compact]);
  var toggleAttribution = useCallback(function () {
    return setShowCompact(function (value) {
      return !value;
    });
  }, []);
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
export default React.memo(AttributionControl);
//# sourceMappingURL=attribution-control.js.map