"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = useMapControl;
exports.mapControlPropTypes = exports.mapControlDefaultProps = void 0;

var _react = require("react");

var PropTypes = _interopRequireWildcard(require("prop-types"));

var _mapContext = _interopRequireDefault(require("./map-context"));

var mapControlDefaultProps = {
  captureScroll: false,
  captureDrag: true,
  captureClick: true,
  captureDoubleClick: true,
  capturePointerMove: false
};
exports.mapControlDefaultProps = mapControlDefaultProps;
var mapControlPropTypes = {
  captureScroll: PropTypes.bool,
  captureDrag: PropTypes.bool,
  captureClick: PropTypes.bool,
  captureDoubleClick: PropTypes.bool,
  capturePointerMove: PropTypes.bool
};
exports.mapControlPropTypes = mapControlPropTypes;

function onMount(thisRef) {
  var ref = thisRef.containerRef.current;
  var eventManager = thisRef.context.eventManager;

  if (!ref || !eventManager) {
    return undefined;
  }

  var events = {
    wheel: function wheel(evt) {
      var props = thisRef.props;

      if (props.captureScroll) {
        evt.stopPropagation();
      }

      if (props.onScroll) {
        props.onScroll(evt, thisRef);
      }
    },
    panstart: function panstart(evt) {
      var props = thisRef.props;

      if (props.captureDrag) {
        evt.stopPropagation();
      }

      if (props.onDragStart) {
        props.onDragStart(evt, thisRef);
      }
    },
    anyclick: function anyclick(evt) {
      var props = thisRef.props;

      if (props.captureClick) {
        evt.stopPropagation();
      }

      if (props.onNativeClick) {
        props.onNativeClick(evt, thisRef);
      }
    },
    click: function click(evt) {
      var props = thisRef.props;

      if (props.captureClick) {
        evt.stopPropagation();
      }

      if (props.onClick) {
        props.onClick(evt, thisRef);
      }
    },
    dblclick: function dblclick(evt) {
      var props = thisRef.props;

      if (props.captureDoubleClick) {
        evt.stopPropagation();
      }

      if (props.onDoubleClick) {
        props.onDoubleClick(evt, thisRef);
      }
    },
    pointermove: function pointermove(evt) {
      var props = thisRef.props;

      if (props.capturePointerMove) {
        evt.stopPropagation();
      }

      if (props.onPointerMove) {
        props.onPointerMove(evt, thisRef);
      }
    }
  };
  eventManager.watch(events, ref);
  return function () {
    eventManager.off(events);
  };
}

function useMapControl() {
  var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var context = (0, _react.useContext)(_mapContext["default"]);
  var containerRef = (0, _react.useRef)(null);

  var _thisRef = (0, _react.useRef)({
    props: props,
    state: {},
    context: context,
    containerRef: containerRef
  });

  var thisRef = _thisRef.current;
  thisRef.props = props;
  thisRef.context = context;
  (0, _react.useEffect)(function () {
    return onMount(thisRef);
  }, [context.eventManager]);
  return thisRef;
}
//# sourceMappingURL=use-map-control.js.map