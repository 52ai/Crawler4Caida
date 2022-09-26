"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _slicedToArray2 = _interopRequireDefault(require("@babel/runtime/helpers/slicedToArray"));

var React = _interopRequireWildcard(require("react"));

var PropTypes = _interopRequireWildcard(require("prop-types"));

var _useMapControl2 = _interopRequireWildcard(require("../components/use-map-control"));

var pixelRatio = typeof window !== 'undefined' && window.devicePixelRatio || 1;
var propTypes = Object.assign({}, _useMapControl2.mapControlPropTypes, {
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
  var _useMapControl = (0, _useMapControl2["default"])(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  var _useState = (0, React.useState)(null),
      _useState2 = (0, _slicedToArray2["default"])(_useState, 2),
      ctx = _useState2[0],
      setDrawingContext = _useState2[1];

  (0, React.useEffect)(function () {
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
var _default = CanvasOverlay;
exports["default"] = _default;
//# sourceMappingURL=canvas-overlay.js.map