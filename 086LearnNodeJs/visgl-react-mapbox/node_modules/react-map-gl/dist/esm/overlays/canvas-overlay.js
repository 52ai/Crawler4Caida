import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";
import * as React from 'react';
import { useState, useEffect } from 'react';
import * as PropTypes from 'prop-types';
import useMapControl, { mapControlPropTypes } from '../components/use-map-control';
var pixelRatio = typeof window !== 'undefined' && window.devicePixelRatio || 1;
var propTypes = Object.assign({}, mapControlPropTypes, {
  redraw: PropTypes.func.isRequired
});
var defaultProps = {
  captureScroll: false,
  captureDrag: false,
  captureClick: false,
  captureDoubleClick: false,
  capturePointerMove: false
};

function CanvasOverlay(props) {
  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var _useState = useState(null),
      _useState2 = _slicedToArray(_useState, 2),
      ctx = _useState2[0],
      setDrawingContext = _useState2[1];

  useEffect(function () {
    setDrawingContext(containerRef.current.getContext('2d'));
  }, []);
  var viewport = context.viewport,
      isDragging = context.isDragging;

  if (ctx) {
    ctx.save();
    ctx.scale(pixelRatio, pixelRatio);
    props.redraw({
      width: viewport.width,
      height: viewport.height,
      ctx: ctx,
      isDragging: isDragging,
      project: viewport.project,
      unproject: viewport.unproject
    });
    ctx.restore();
  }

  return React.createElement("canvas", {
    ref: containerRef,
    width: viewport.width * pixelRatio,
    height: viewport.height * pixelRatio,
    style: {
      width: "".concat(viewport.width, "px"),
      height: "".concat(viewport.height, "px"),
      position: 'absolute',
      left: 0,
      top: 0
    }
  });
}

CanvasOverlay.propTypes = propTypes;
CanvasOverlay.defaultProps = defaultProps;
export default CanvasOverlay;
//# sourceMappingURL=canvas-overlay.js.map