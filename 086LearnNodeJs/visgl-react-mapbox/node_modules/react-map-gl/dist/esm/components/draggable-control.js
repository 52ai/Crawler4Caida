import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
export var draggableControlPropTypes = Object.assign({}, mapControlPropTypes, {
  draggable: PropTypes.bool,
  onDrag: PropTypes.func,
  onDragEnd: PropTypes.func,
  onDragStart: PropTypes.func,
  offsetLeft: PropTypes.number,
  offsetTop: PropTypes.number
});
export var draggableControlDefaultProps = Object.assign({}, mapControlDefaultProps, {
  draggable: false,
  offsetLeft: 0,
  offsetTop: 0
});

function getDragEventPosition(event) {
  var _event$offsetCenter = event.offsetCenter,
      x = _event$offsetCenter.x,
      y = _event$offsetCenter.y;
  return [x, y];
}

function getDragEventOffset(event, container) {
  var _event$center = event.center,
      x = _event$center.x,
      y = _event$center.y;

  if (container) {
    var rect = container.getBoundingClientRect();
    return [rect.left - x, rect.top - y];
  }

  return null;
}

function getDragLngLat(dragPos, dragOffset, props, context) {
  var x = dragPos[0] + dragOffset[0] - props.offsetLeft;
  var y = dragPos[1] + dragOffset[1] - props.offsetTop;
  return context.viewport.unproject([x, y]);
}

function onDragStart(event, _ref) {
  var props = _ref.props,
      callbacks = _ref.callbacks,
      state = _ref.state,
      context = _ref.context,
      containerRef = _ref.containerRef;
  var draggable = props.draggable;

  if (!draggable) {
    return;
  }

  event.stopPropagation();
  var dragPos = getDragEventPosition(event);
  var dragOffset = getDragEventOffset(event, containerRef.current);
  state.setDragPos(dragPos);
  state.setDragOffset(dragOffset);

  if (callbacks.onDragStart && dragOffset) {
    var callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDragStart(callbackEvent);
  }
}

function onDrag(event, _ref2) {
  var props = _ref2.props,
      callbacks = _ref2.callbacks,
      state = _ref2.state,
      context = _ref2.context;
  event.stopPropagation();
  var dragPos = getDragEventPosition(event);
  state.setDragPos(dragPos);
  var dragOffset = state.dragOffset;

  if (callbacks.onDrag && dragOffset) {
    var callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDrag(callbackEvent);
  }
}

function onDragEnd(event, _ref3) {
  var props = _ref3.props,
      callbacks = _ref3.callbacks,
      state = _ref3.state,
      context = _ref3.context;
  event.stopPropagation();
  var dragPos = state.dragPos,
      dragOffset = state.dragOffset;
  state.setDragPos(null);
  state.setDragOffset(null);

  if (callbacks.onDragEnd && dragPos && dragOffset) {
    var callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDragEnd(callbackEvent);
  }
}

function onDragCancel(event, _ref4) {
  var state = _ref4.state;
  event.stopPropagation();
  state.setDragPos(null);
  state.setDragOffset(null);
}

function registerEvents(thisRef) {
  var eventManager = thisRef.context.eventManager;

  if (!eventManager || !thisRef.state.dragPos) {
    return undefined;
  }

  var events = {
    panmove: function panmove(evt) {
      return onDrag(evt, thisRef);
    },
    panend: function panend(evt) {
      return onDragEnd(evt, thisRef);
    },
    pancancel: function pancancel(evt) {
      return onDragCancel(evt, thisRef);
    }
  };
  eventManager.watch(events);
  return function () {
    eventManager.off(events);
  };
}

export default function useDraggableControl(props) {
  var _useState = useState(null),
      _useState2 = _slicedToArray(_useState, 2),
      dragPos = _useState2[0],
      setDragPos = _useState2[1];

  var _useState3 = useState(null),
      _useState4 = _slicedToArray(_useState3, 2),
      dragOffset = _useState4[0],
      setDragOffset = _useState4[1];

  var thisRef = useMapControl(_objectSpread(_objectSpread({}, props), {}, {
    onDragStart: onDragStart
  }));
  thisRef.callbacks = props;
  thisRef.state.dragPos = dragPos;
  thisRef.state.setDragPos = setDragPos;
  thisRef.state.dragOffset = dragOffset;
  thisRef.state.setDragOffset = setDragOffset;
  useEffect(function () {
    return registerEvents(thisRef);
  }, [thisRef.context.eventManager, Boolean(dragPos)]);
  return thisRef;
}
//# sourceMappingURL=draggable-control.js.map