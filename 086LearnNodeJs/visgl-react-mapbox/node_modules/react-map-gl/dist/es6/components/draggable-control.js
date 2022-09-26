import * as PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
export const draggableControlPropTypes = Object.assign({}, mapControlPropTypes, {
  draggable: PropTypes.bool,
  onDrag: PropTypes.func,
  onDragEnd: PropTypes.func,
  onDragStart: PropTypes.func,
  offsetLeft: PropTypes.number,
  offsetTop: PropTypes.number
});
export const draggableControlDefaultProps = Object.assign({}, mapControlDefaultProps, {
  draggable: false,
  offsetLeft: 0,
  offsetTop: 0
});

function getDragEventPosition(event) {
  const {
    offsetCenter: {
      x,
      y
    }
  } = event;
  return [x, y];
}

function getDragEventOffset(event, container) {
  const {
    center: {
      x,
      y
    }
  } = event;

  if (container) {
    const rect = container.getBoundingClientRect();
    return [rect.left - x, rect.top - y];
  }

  return null;
}

function getDragLngLat(dragPos, dragOffset, props, context) {
  const x = dragPos[0] + dragOffset[0] - props.offsetLeft;
  const y = dragPos[1] + dragOffset[1] - props.offsetTop;
  return context.viewport.unproject([x, y]);
}

function onDragStart(event, {
  props,
  callbacks,
  state,
  context,
  containerRef
}) {
  const {
    draggable
  } = props;

  if (!draggable) {
    return;
  }

  event.stopPropagation();
  const dragPos = getDragEventPosition(event);
  const dragOffset = getDragEventOffset(event, containerRef.current);
  state.setDragPos(dragPos);
  state.setDragOffset(dragOffset);

  if (callbacks.onDragStart && dragOffset) {
    const callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDragStart(callbackEvent);
  }
}

function onDrag(event, {
  props,
  callbacks,
  state,
  context
}) {
  event.stopPropagation();
  const dragPos = getDragEventPosition(event);
  state.setDragPos(dragPos);
  const {
    dragOffset
  } = state;

  if (callbacks.onDrag && dragOffset) {
    const callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDrag(callbackEvent);
  }
}

function onDragEnd(event, {
  props,
  callbacks,
  state,
  context
}) {
  event.stopPropagation();
  const {
    dragPos,
    dragOffset
  } = state;
  state.setDragPos(null);
  state.setDragOffset(null);

  if (callbacks.onDragEnd && dragPos && dragOffset) {
    const callbackEvent = Object.assign({}, event);
    callbackEvent.lngLat = getDragLngLat(dragPos, dragOffset, props, context);
    callbacks.onDragEnd(callbackEvent);
  }
}

function onDragCancel(event, {
  state
}) {
  event.stopPropagation();
  state.setDragPos(null);
  state.setDragOffset(null);
}

function registerEvents(thisRef) {
  const {
    eventManager
  } = thisRef.context;

  if (!eventManager || !thisRef.state.dragPos) {
    return undefined;
  }

  const events = {
    panmove: evt => onDrag(evt, thisRef),
    panend: evt => onDragEnd(evt, thisRef),
    pancancel: evt => onDragCancel(evt, thisRef)
  };
  eventManager.watch(events);
  return () => {
    eventManager.off(events);
  };
}

export default function useDraggableControl(props) {
  const [dragPos, setDragPos] = useState(null);
  const [dragOffset, setDragOffset] = useState(null);
  const thisRef = useMapControl({ ...props,
    onDragStart
  });
  thisRef.callbacks = props;
  thisRef.state.dragPos = dragPos;
  thisRef.state.setDragPos = setDragPos;
  thisRef.state.dragOffset = dragOffset;
  thisRef.state.setDragOffset = setDragOffset;
  useEffect(() => registerEvents(thisRef), [thisRef.context.eventManager, Boolean(dragPos)]);
  return thisRef;
}
//# sourceMappingURL=draggable-control.js.map