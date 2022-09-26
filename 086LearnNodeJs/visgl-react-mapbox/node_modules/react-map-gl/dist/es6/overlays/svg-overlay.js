import * as React from 'react';
import * as PropTypes from 'prop-types';
import useMapControl, { mapControlPropTypes } from '../components/use-map-control';
const propTypes = Object.assign({}, mapControlPropTypes, {
  redraw: PropTypes.func.isRequired,
  style: PropTypes.object
});
const defaultProps = {
  captureScroll: false,
  captureDrag: false,
  captureClick: false,
  captureDoubleClick: false,
  capturePointerMove: false
};

function SVGOverlay(props) {
  const {
    context,
    containerRef
  } = useMapControl(props);
  const {
    viewport,
    isDragging
  } = context;
  const style = {
    position: 'absolute',
    left: 0,
    top: 0,
    ...props.style
  };
  return React.createElement("svg", {
    width: viewport.width,
    height: viewport.height,
    ref: containerRef,
    style: style
  }, props.redraw({
    width: viewport.width,
    height: viewport.height,
    isDragging,
    project: viewport.project,
    unproject: viewport.unproject
  }));
}

SVGOverlay.propTypes = propTypes;
SVGOverlay.defaultProps = defaultProps;
export default SVGOverlay;
//# sourceMappingURL=svg-overlay.js.map