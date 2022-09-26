import * as React from 'react';
import { useState, useEffect } from 'react';
import * as PropTypes from 'prop-types';
import useMapControl, { mapControlPropTypes } from '../components/use-map-control';
const pixelRatio = typeof window !== 'undefined' && window.devicePixelRatio || 1;
const propTypes = Object.assign({}, mapControlPropTypes, {
  redraw: PropTypes.func.isRequired
});
const defaultProps = {
  captureScroll: false,
  captureDrag: false,
  captureClick: false,
  captureDoubleClick: false,
  capturePointerMove: false
};

function CanvasOverlay(props) {
  const {
    context,
    containerRef
  } = useMapControl(props);
  const [ctx, setDrawingContext] = useState(null);
  useEffect(() => {
    setDrawingContext(containerRef.current.getContext('2d'));
  }, []);
  const {
    viewport,
    isDragging
  } = context;

  if (ctx) {
    ctx.save();
    ctx.scale(pixelRatio, pixelRatio);
    props.redraw({
      width: viewport.width,
      height: viewport.height,
      ctx,
      isDragging,
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