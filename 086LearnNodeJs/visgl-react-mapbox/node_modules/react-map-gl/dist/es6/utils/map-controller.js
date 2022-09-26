import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import MapState from './map-state';
import { LinearInterpolator } from './transition';
import TransitionManager, { TRANSITION_EVENTS } from './transition-manager';
const NO_TRANSITION_PROPS = {
  transitionDuration: 0
};
export const LINEAR_TRANSITION_PROPS = {
  transitionDuration: 300,
  transitionEasing: t => t,
  transitionInterpolator: new LinearInterpolator(),
  transitionInterruption: TRANSITION_EVENTS.BREAK
};
const DEFAULT_INERTIA = 300;

const INERTIA_EASING = t => 1 - (1 - t) * (1 - t);

const EVENT_TYPES = {
  WHEEL: ['wheel'],
  PAN: ['panstart', 'panmove', 'panend'],
  PINCH: ['pinchstart', 'pinchmove', 'pinchend'],
  TRIPLE_PAN: ['tripanstart', 'tripanmove', 'tripanend'],
  DOUBLE_TAP: ['doubletap'],
  KEYBOARD: ['keydown']
};
export default class MapController {
  constructor() {
    _defineProperty(this, "events", []);

    _defineProperty(this, "scrollZoom", true);

    _defineProperty(this, "dragPan", true);

    _defineProperty(this, "dragRotate", true);

    _defineProperty(this, "doubleClickZoom", true);

    _defineProperty(this, "touchZoom", true);

    _defineProperty(this, "touchRotate", false);

    _defineProperty(this, "keyboard", true);

    _defineProperty(this, "_interactionState", {
      isDragging: false
    });

    _defineProperty(this, "_events", {});

    _defineProperty(this, "_setInteractionState", newState => {
      Object.assign(this._interactionState, newState);

      if (this.onStateChange) {
        this.onStateChange(this._interactionState);
      }
    });

    _defineProperty(this, "_onTransition", (newViewport, oldViewport) => {
      this.onViewportChange(newViewport, this._interactionState, oldViewport);
    });

    this.handleEvent = this.handleEvent.bind(this);
    this._transitionManager = new TransitionManager({
      onViewportChange: this._onTransition,
      onStateChange: this._setInteractionState
    });
  }

  handleEvent(event) {
    this.mapState = this.getMapState();
    const eventStartBlocked = this._eventStartBlocked;

    switch (event.type) {
      case 'panstart':
        return eventStartBlocked ? false : this._onPanStart(event);

      case 'panmove':
        return this._onPan(event);

      case 'panend':
        return this._onPanEnd(event);

      case 'pinchstart':
        return eventStartBlocked ? false : this._onPinchStart(event);

      case 'pinchmove':
        return this._onPinch(event);

      case 'pinchend':
        return this._onPinchEnd(event);

      case 'tripanstart':
        return eventStartBlocked ? false : this._onTriplePanStart(event);

      case 'tripanmove':
        return this._onTriplePan(event);

      case 'tripanend':
        return this._onTriplePanEnd(event);

      case 'doubletap':
        return this._onDoubleTap(event);

      case 'wheel':
        return this._onWheel(event);

      case 'keydown':
        return this._onKeyDown(event);

      default:
        return false;
    }
  }

  getCenter(event) {
    const {
      offsetCenter: {
        x,
        y
      }
    } = event;
    return [x, y];
  }

  isFunctionKeyPressed(event) {
    const {
      srcEvent
    } = event;
    return Boolean(srcEvent.metaKey || srcEvent.altKey || srcEvent.ctrlKey || srcEvent.shiftKey);
  }

  blockEvents(timeout) {
    const timer = setTimeout(() => {
      if (this._eventStartBlocked === timer) {
        this._eventStartBlocked = null;
      }
    }, timeout);
    this._eventStartBlocked = timer;
  }

  updateViewport(newMapState, extraProps, interactionState) {
    const oldViewport = this.mapState instanceof MapState ? this.mapState.getViewportProps() : this.mapState;
    const newViewport = { ...newMapState.getViewportProps(),
      ...extraProps
    };
    const viewStateChanged = Object.keys(newViewport).some(key => oldViewport[key] !== newViewport[key]);
    this._state = newMapState.getState();

    this._setInteractionState(interactionState);

    if (viewStateChanged) {
      this.onViewportChange(newViewport, this._interactionState, oldViewport);
    }
  }

  getMapState(overrides) {
    return new MapState({ ...this.mapStateProps,
      ...this._state,
      ...overrides
    });
  }

  isDragging() {
    return this._interactionState.isDragging;
  }

  setOptions(options) {
    const {
      onViewportChange,
      onStateChange,
      eventManager = this.eventManager,
      isInteractive = true,
      scrollZoom = this.scrollZoom,
      dragPan = this.dragPan,
      dragRotate = this.dragRotate,
      doubleClickZoom = this.doubleClickZoom,
      touchZoom = this.touchZoom,
      touchRotate = this.touchRotate,
      keyboard = this.keyboard
    } = options;
    this.onViewportChange = onViewportChange;
    this.onStateChange = onStateChange;
    const prevOptions = this.mapStateProps || {};
    const dimensionChanged = prevOptions.height !== options.height || prevOptions.width !== options.width;
    this.mapStateProps = options;

    if (dimensionChanged) {
      this.mapState = prevOptions;
      this.updateViewport(new MapState(options));
    }

    this._transitionManager.processViewportChange(options);

    if (this.eventManager !== eventManager) {
      this.eventManager = eventManager;
      this._events = {};
      this.toggleEvents(this.events, true);
    }

    this.toggleEvents(EVENT_TYPES.WHEEL, isInteractive && Boolean(scrollZoom));
    this.toggleEvents(EVENT_TYPES.PAN, isInteractive && Boolean(dragPan || dragRotate));
    this.toggleEvents(EVENT_TYPES.PINCH, isInteractive && Boolean(touchZoom || touchRotate));
    this.toggleEvents(EVENT_TYPES.TRIPLE_PAN, isInteractive && Boolean(touchRotate));
    this.toggleEvents(EVENT_TYPES.DOUBLE_TAP, isInteractive && Boolean(doubleClickZoom));
    this.toggleEvents(EVENT_TYPES.KEYBOARD, isInteractive && Boolean(keyboard));
    this.scrollZoom = scrollZoom;
    this.dragPan = dragPan;
    this.dragRotate = dragRotate;
    this.doubleClickZoom = doubleClickZoom;
    this.touchZoom = touchZoom;
    this.touchRotate = touchRotate;
    this.keyboard = keyboard;
  }

  toggleEvents(eventNames, enabled) {
    if (this.eventManager) {
      eventNames.forEach(eventName => {
        if (this._events[eventName] !== enabled) {
          this._events[eventName] = enabled;

          if (enabled) {
            this.eventManager.on(eventName, this.handleEvent);
          } else {
            this.eventManager.off(eventName, this.handleEvent);
          }
        }
      });
    }
  }

  _onPanStart(event) {
    const pos = this.getCenter(event);
    this._panRotate = this.isFunctionKeyPressed(event) || event.rightButton;
    const newMapState = this._panRotate ? this.mapState.rotateStart({
      pos
    }) : this.mapState.panStart({
      pos
    });
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isDragging: true
    });
    return true;
  }

  _onPan(event) {
    if (!this.isDragging()) {
      return false;
    }

    return this._panRotate ? this._onPanRotate(event) : this._onPanMove(event);
  }

  _onPanEnd(event) {
    if (!this.isDragging()) {
      return false;
    }

    return this._panRotate ? this._onPanRotateEnd(event) : this._onPanMoveEnd(event);
  }

  _onPanMove(event) {
    if (!this.dragPan) {
      return false;
    }

    const pos = this.getCenter(event);
    const newMapState = this.mapState.pan({
      pos
    });
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isPanning: true
    });
    return true;
  }

  _onPanMoveEnd(event) {
    if (this.dragPan) {
      const {
        inertia = DEFAULT_INERTIA
      } = this.dragPan;

      if (inertia && event.velocity) {
        const pos = this.getCenter(event);
        const endPos = [pos[0] + event.velocityX * inertia / 2, pos[1] + event.velocityY * inertia / 2];
        const newControllerState = this.mapState.pan({
          pos: endPos
        }).panEnd();
        this.updateViewport(newControllerState, { ...LINEAR_TRANSITION_PROPS,
          transitionDuration: inertia,
          transitionEasing: INERTIA_EASING
        }, {
          isDragging: false,
          isPanning: true
        });
        return true;
      }
    }

    const newMapState = this.mapState.panEnd();
    this.updateViewport(newMapState, null, {
      isDragging: false,
      isPanning: false
    });
    return true;
  }

  _onPanRotate(event) {
    if (!this.dragRotate) {
      return false;
    }

    const pos = this.getCenter(event);
    const newMapState = this.mapState.rotate({
      pos
    });
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isRotating: true
    });
    return true;
  }

  _onPanRotateEnd(event) {
    if (this.dragRotate) {
      const {
        inertia = DEFAULT_INERTIA
      } = this.dragRotate;

      if (inertia && event.velocity) {
        const pos = this.getCenter(event);
        const endPos = [pos[0] + event.velocityX * inertia / 2, pos[1] + event.velocityY * inertia / 2];
        const newControllerState = this.mapState.rotate({
          pos: endPos
        }).rotateEnd();
        this.updateViewport(newControllerState, { ...LINEAR_TRANSITION_PROPS,
          transitionDuration: inertia,
          transitionEasing: INERTIA_EASING
        }, {
          isDragging: false,
          isRotating: true
        });
        return true;
      }
    }

    const newMapState = this.mapState.panEnd();
    this.updateViewport(newMapState, null, {
      isDragging: false,
      isRotating: false
    });
    return true;
  }

  _onWheel(event) {
    if (!this.scrollZoom) {
      return false;
    }

    const {
      speed = 0.01,
      smooth = false
    } = this.scrollZoom;
    event.preventDefault();
    const pos = this.getCenter(event);
    const {
      delta
    } = event;
    let scale = 2 / (1 + Math.exp(-Math.abs(delta * speed)));

    if (delta < 0 && scale !== 0) {
      scale = 1 / scale;
    }

    const newMapState = this.mapState.zoom({
      pos,
      scale
    });

    if (newMapState.getViewportProps().zoom === this.mapStateProps.zoom) {
      return false;
    }

    this.updateViewport(newMapState, { ...LINEAR_TRANSITION_PROPS,
      transitionInterpolator: new LinearInterpolator({
        around: pos
      }),
      transitionDuration: smooth ? 250 : 1
    }, {
      isPanning: true,
      isZooming: true
    });
    return true;
  }

  _onPinchStart(event) {
    const pos = this.getCenter(event);
    const newMapState = this.mapState.zoomStart({
      pos
    }).rotateStart({
      pos
    });
    this._startPinchRotation = event.rotation;
    this._lastPinchEvent = event;
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isDragging: true
    });
    return true;
  }

  _onPinch(event) {
    if (!this.isDragging()) {
      return false;
    }

    if (!this.touchZoom && !this.touchRotate) {
      return false;
    }

    let newMapState = this.mapState;

    if (this.touchZoom) {
      const {
        scale
      } = event;
      const pos = this.getCenter(event);
      newMapState = newMapState.zoom({
        pos,
        scale
      });
    }

    if (this.touchRotate) {
      const {
        rotation
      } = event;
      newMapState = newMapState.rotate({
        deltaAngleX: this._startPinchRotation - rotation
      });
    }

    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isDragging: true,
      isPanning: Boolean(this.touchZoom),
      isZooming: Boolean(this.touchZoom),
      isRotating: Boolean(this.touchRotate)
    });
    this._lastPinchEvent = event;
    return true;
  }

  _onPinchEnd(event) {
    if (!this.isDragging()) {
      return false;
    }

    if (this.touchZoom) {
      const {
        inertia = DEFAULT_INERTIA
      } = this.touchZoom;
      const {
        _lastPinchEvent
      } = this;

      if (inertia && _lastPinchEvent && event.scale !== _lastPinchEvent.scale) {
        const pos = this.getCenter(event);
        let newMapState = this.mapState.rotateEnd();
        const z = Math.log2(event.scale);

        const velocityZ = (z - Math.log2(_lastPinchEvent.scale)) / (event.deltaTime - _lastPinchEvent.deltaTime);

        const endScale = Math.pow(2, z + velocityZ * inertia / 2);
        newMapState = newMapState.zoom({
          pos,
          scale: endScale
        }).zoomEnd();
        this.updateViewport(newMapState, { ...LINEAR_TRANSITION_PROPS,
          transitionInterpolator: new LinearInterpolator({
            around: pos
          }),
          transitionDuration: inertia,
          transitionEasing: INERTIA_EASING
        }, {
          isDragging: false,
          isPanning: Boolean(this.touchZoom),
          isZooming: Boolean(this.touchZoom),
          isRotating: false
        });
        this.blockEvents(inertia);
        return true;
      }
    }

    const newMapState = this.mapState.zoomEnd().rotateEnd();
    this._state.startPinchRotation = 0;
    this.updateViewport(newMapState, null, {
      isDragging: false,
      isPanning: false,
      isZooming: false,
      isRotating: false
    });
    this._startPinchRotation = null;
    this._lastPinchEvent = null;
    return true;
  }

  _onTriplePanStart(event) {
    const pos = this.getCenter(event);
    const newMapState = this.mapState.rotateStart({
      pos
    });
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isDragging: true
    });
    return true;
  }

  _onTriplePan(event) {
    if (!this.isDragging()) {
      return false;
    }

    if (!this.touchRotate) {
      return false;
    }

    const pos = this.getCenter(event);
    pos[0] -= event.deltaX;
    const newMapState = this.mapState.rotate({
      pos
    });
    this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
      isRotating: true
    });
    return true;
  }

  _onTriplePanEnd(event) {
    if (!this.isDragging()) {
      return false;
    }

    if (this.touchRotate) {
      const {
        inertia = DEFAULT_INERTIA
      } = this.touchRotate;

      if (inertia && event.velocityY) {
        const pos = this.getCenter(event);
        const endPos = [pos[0], pos[1] += event.velocityY * inertia / 2];
        const newMapState = this.mapState.rotate({
          pos: endPos
        });
        this.updateViewport(newMapState, { ...LINEAR_TRANSITION_PROPS,
          transitionDuration: inertia,
          transitionEasing: INERTIA_EASING
        }, {
          isDragging: false,
          isRotating: true
        });
        this.blockEvents(inertia);
        return false;
      }
    }

    const newMapState = this.mapState.rotateEnd();
    this.updateViewport(newMapState, null, {
      isDragging: false,
      isRotating: false
    });
    return true;
  }

  _onDoubleTap(event) {
    if (!this.doubleClickZoom) {
      return false;
    }

    const pos = this.getCenter(event);
    const isZoomOut = this.isFunctionKeyPressed(event);
    const newMapState = this.mapState.zoom({
      pos,
      scale: isZoomOut ? 0.5 : 2
    });
    this.updateViewport(newMapState, Object.assign({}, LINEAR_TRANSITION_PROPS, {
      transitionInterpolator: new LinearInterpolator({
        around: pos
      })
    }), {
      isZooming: true
    });
    return true;
  }

  _onKeyDown(event) {
    if (!this.keyboard) {
      return false;
    }

    const funcKey = this.isFunctionKeyPressed(event);
    const {
      zoomSpeed = 2,
      moveSpeed = 100,
      rotateSpeedX = 15,
      rotateSpeedY = 10
    } = this.keyboard;
    const {
      mapStateProps
    } = this;
    let newMapState;

    switch (event.srcEvent.keyCode) {
      case 189:
        if (funcKey) {
          newMapState = this.getMapState({
            zoom: mapStateProps.zoom - Math.log2(zoomSpeed) - 1
          });
        } else {
          newMapState = this.getMapState({
            zoom: mapStateProps.zoom - Math.log2(zoomSpeed)
          });
        }

        break;

      case 187:
        if (funcKey) {
          newMapState = this.getMapState({
            zoom: mapStateProps.zoom + Math.log2(zoomSpeed) + 1
          });
        } else {
          newMapState = this.getMapState({
            zoom: mapStateProps.zoom + Math.log2(zoomSpeed)
          });
        }

        break;

      case 37:
        if (funcKey) {
          newMapState = this.getMapState({
            bearing: mapStateProps.bearing - rotateSpeedX
          });
        } else {
          newMapState = this.mapState.pan({
            pos: [moveSpeed, 0],
            startPos: [0, 0]
          });
        }

        break;

      case 39:
        if (funcKey) {
          newMapState = this.getMapState({
            bearing: mapStateProps.bearing + rotateSpeedX
          });
        } else {
          newMapState = this.mapState.pan({
            pos: [-moveSpeed, 0],
            startPos: [0, 0]
          });
        }

        break;

      case 38:
        if (funcKey) {
          newMapState = this.getMapState({
            pitch: mapStateProps.pitch + rotateSpeedY
          });
        } else {
          newMapState = this.mapState.pan({
            pos: [0, moveSpeed],
            startPos: [0, 0]
          });
        }

        break;

      case 40:
        if (funcKey) {
          newMapState = this.getMapState({
            pitch: mapStateProps.pitch - rotateSpeedY
          });
        } else {
          newMapState = this.mapState.pan({
            pos: [0, -moveSpeed],
            startPos: [0, 0]
          });
        }

        break;

      default:
        return false;
    }

    return this.updateViewport(newMapState, LINEAR_TRANSITION_PROPS);
  }

}
//# sourceMappingURL=map-controller.js.map