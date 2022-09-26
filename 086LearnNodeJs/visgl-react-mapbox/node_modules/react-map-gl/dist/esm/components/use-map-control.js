import { useContext, useRef, useEffect } from 'react';
import * as PropTypes from 'prop-types';
import MapContext from './map-context';
export var mapControlDefaultProps = {
  captureScroll: false,
  captureDrag: true,
  captureClick: true,
  captureDoubleClick: true,
  capturePointerMove: false
};
export var mapControlPropTypes = {
  captureScroll: PropTypes.bool,
  captureDrag: PropTypes.bool,
  captureClick: PropTypes.bool,
  captureDoubleClick: PropTypes.bool,
  capturePointerMove: PropTypes.bool
};

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

export default function useMapControl() {
  var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  var context = useContext(MapContext);
  var containerRef = useRef(null);

  var _thisRef = useRef({
    props: props,
    state: {},
    context: context,
    containerRef: containerRef
  });

  var thisRef = _thisRef.current;
  thisRef.props = props;
  thisRef.context = context;
  useEffect(function () {
    return onMount(thisRef);
  }, [context.eventManager]);
  return thisRef;
}
//# sourceMappingURL=use-map-control.js.map