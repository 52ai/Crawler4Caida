import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import * as PropTypes from 'prop-types';
import useMapControl, { mapControlPropTypes } from '../components/use-map-control';
var propTypes = Object.assign({}, mapControlPropTypes, {
  redraw: PropTypes.func.isRequired,
  style: PropTypes.object
});
var defaultProps = {
  captureScroll: false,
  captureDrag: false,
  captureClick: false,
  captureDoubleClick: false,
  capturePointerMove: false
};

function HTMLOverlay(props) {
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var viewport = context.viewport,
      isDragging = context.isDragging;

  var style = _objectSpread({
    position: 'absolute',
    left: 0,
    top: 0,
    width: viewport.width,
    height: viewport.height
  }, props.style);

  return React.createElement("div", {
    ref: containerRef,
    style: style
  }, props.redraw({
    width: viewport.width,
    height: viewport.height,
    isDragging: isDragging,
    project: viewport.project,
    unproject: viewport.unproject
  }));
}

HTMLOverlay.propTypes = propTypes;
HTMLOverlay.defaultProps = defaultProps;
export default HTMLOverlay;
//# sourceMappingURL=html-overlay.js.map