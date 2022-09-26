import _classCallCheck from "@babel/runtime/helpers/esm/classCallCheck";
import _createClass from "@babel/runtime/helpers/esm/createClass";
import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import MapState from './map-state';
import { LinearInterpolator } from './transition';
import TransitionManager, { TRANSITION_EVENTS } from './transition-manager';
var NO_TRANSITION_PROPS = {
  transitionDuration: 0
};
export var LINEAR_TRANSITION_PROPS = {
  transitionDuration: 300,
  transitionEasing: function transitionEasing(t) {
    return t;
  },
  transitionInterpolator: new LinearInterpolator(),
  transitionInterruption: TRANSITION_EVENTS.BREAK
};
var DEFAULT_INERTIA = 300;

var INERTIA_EASING = function INERTIA_EASING(t) {
  return 1 - (1 - t) * (1 - t);
};

var EVENT_TYPES = {
  WHEEL: ['wheel'],
  PAN: ['panstart', 'panmove', 'panend'],
  PINCH: ['pinchstart', 'pinchmove', 'pinchend'],
  TRIPLE_PAN: ['tripanstart', 'tripanmove', 'tripanend'],
  DOUBLE_TAP: ['doubletap'],
  KEYBOARD: ['keydown']
};

var MapController = function () {
  function MapController() {
    var _this = this;

    _classCallCheck(this, MapController);

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

    _defineProperty(this, "_setInteractionState", function (newState) {
      Object.assign(_this._interactionState, newState);

      if (_this.onStateChange) {
        _this.onStateChange(_this._interactionState);
      }
    });

    _defineProperty(this, "_onTransition", function (newViewport, oldViewport) {
      _this.onViewportChange(newViewport, _this._interactionState, oldViewport);
    });

    this.handleEvent = this.handleEvent.bind(this);
    this._transitionManager = new TransitionManager({
      onViewportChange: this._onTransition,
      onStateChange: this._setInteractionState
    });
  }

  _createClass(MapController, [{
    key: "handleEvent",
    value: function handleEvent(event) {
      this.mapState = this.getMapState();
      var eventStartBlocked = this._eventStartBlocked;

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
  }, {
    key: "getCenter",
    value: function getCenter(event) {
      var _event$offsetCenter = event.offsetCenter,
          x = _event$offsetCenter.x,
          y = _event$offsetCenter.y;
      return [x, y];
    }
  }, {
    key: "isFunctionKeyPressed",
    value: function isFunctionKeyPressed(event) {
      var srcEvent = event.srcEvent;
      return Boolean(srcEvent.metaKey || srcEvent.altKey || srcEvent.ctrlKey || srcEvent.shiftKey);
    }
  }, {
    key: "blockEvents",
    value: function blockEvents(timeout) {
      var _this2 = this;

      var timer = setTimeout(function () {
        if (_this2._eventStartBlocked === timer) {
          _this2._eventStartBlocked = null;
        }
      }, timeout);
      this._eventStartBlocked = timer;
    }
  }, {
    key: "updateViewport",
    value: function updateViewport(newMapState, extraProps, interactionState) {
      var oldViewport = this.mapState instanceof MapState ? this.mapState.getViewportProps() : this.mapState;

      var newViewport = _objectSpread(_objectSpread({}, newMapState.getViewportProps()), extraProps);

      var viewStateChanged = Object.keys(newViewport).some(function (key) {
        return oldViewport[key] !== newViewport[key];
      });
      this._state = newMapState.getState();

      this._setInteractionState(interactionState);

      if (viewStateChanged) {
        this.onViewportChange(newViewport, this._interactionState, oldViewport);
      }
    }
  }, {
    key: "getMapState",
    value: function getMapState(overrides) {
      return new MapState(_objectSpread(_objectSpread(_objectSpread({}, this.mapStateProps), this._state), overrides));
    }
  }, {
    key: "isDragging",
    value: function isDragging() {
      return this._interactionState.isDragging;
    }
  }, {
    key: "setOptions",
    value: function setOptions(options) {
      var onViewportChange = options.onViewportChange,
          onStateChange = options.onStateChange,
          _options$eventManager = options.eventManager,
          eventManager = _options$eventManager === void 0 ? this.eventManager : _options$eventManager,
          _options$isInteractiv = options.isInteractive,
          isInteractive = _options$isInteractiv === void 0 ? true : _options$isInteractiv,
          _options$scrollZoom = options.scrollZoom,
          scrollZoom = _options$scrollZoom === void 0 ? this.scrollZoom : _options$scrollZoom,
          _options$dragPan = options.dragPan,
          dragPan = _options$dragPan === void 0 ? this.dragPan : _options$dragPan,
          _options$dragRotate = options.dragRotate,
          dragRotate = _options$dragRotate === void 0 ? this.dragRotate : _options$dragRotate,
          _options$doubleClickZ = options.doubleClickZoom,
          doubleClickZoom = _options$doubleClickZ === void 0 ? this.doubleClickZoom : _options$doubleClickZ,
          _options$touchZoom = options.touchZoom,
          touchZoom = _options$touchZoom === void 0 ? this.touchZoom : _options$touchZoom,
          _options$touchRotate = options.touchRotate,
          touchRotate = _options$touchRotate === void 0 ? this.touchRotate : _options$touchRotate,
          _options$keyboard = options.keyboard,
          keyboard = _options$keyboard === void 0 ? this.keyboard : _options$keyboard;
      this.onViewportChange = onViewportChange;
      this.onStateChange = onStateChange;
      var prevOptions = this.mapStateProps || {};
      var dimensionChanged = prevOptions.height !== options.height || prevOptions.width !== options.width;
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
  }, {
    key: "toggleEvents",
    value: function toggleEvents(eventNames, enabled) {
      var _this3 = this;

      if (this.eventManager) {
        eventNames.forEach(function (eventName) {
          if (_this3._events[eventName] !== enabled) {
            _this3._events[eventName] = enabled;

            if (enabled) {
              _this3.eventManager.on(eventName, _this3.handleEvent);
            } else {
              _this3.eventManager.off(eventName, _this3.handleEvent);
            }
          }
        });
      }
    }
  }, {
    key: "_onPanStart",
    value: function _onPanStart(event) {
      var pos = this.getCenter(event);
      this._panRotate = this.isFunctionKeyPressed(event) || event.rightButton;
      var newMapState = this._panRotate ? this.mapState.rotateStart({
        pos: pos
      }) : this.mapState.panStart({
        pos: pos
      });
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isDragging: true
      });
      return true;
    }
  }, {
    key: "_onPan",
    value: function _onPan(event) {
      if (!this.isDragging()) {
        return false;
      }

      return this._panRotate ? this._onPanRotate(event) : this._onPanMove(event);
    }
  }, {
    key: "_onPanEnd",
    value: function _onPanEnd(event) {
      if (!this.isDragging()) {
        return false;
      }

      return this._panRotate ? this._onPanRotateEnd(event) : this._onPanMoveEnd(event);
    }
  }, {
    key: "_onPanMove",
    value: function _onPanMove(event) {
      if (!this.dragPan) {
        return false;
      }

      var pos = this.getCenter(event);
      var newMapState = this.mapState.pan({
        pos: pos
      });
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isPanning: true
      });
      return true;
    }
  }, {
    key: "_onPanMoveEnd",
    value: function _onPanMoveEnd(event) {
      if (this.dragPan) {
        var _this$dragPan$inertia = this.dragPan.inertia,
            inertia = _this$dragPan$inertia === void 0 ? DEFAULT_INERTIA : _this$dragPan$inertia;

        if (inertia && event.velocity) {
          var pos = this.getCenter(event);
          var endPos = [pos[0] + event.velocityX * inertia / 2, pos[1] + event.velocityY * inertia / 2];
          var newControllerState = this.mapState.pan({
            pos: endPos
          }).panEnd();
          this.updateViewport(newControllerState, _objectSpread(_objectSpread({}, LINEAR_TRANSITION_PROPS), {}, {
            transitionDuration: inertia,
            transitionEasing: INERTIA_EASING
          }), {
            isDragging: false,
            isPanning: true
          });
          return true;
        }
      }

      var newMapState = this.mapState.panEnd();
      this.updateViewport(newMapState, null, {
        isDragging: false,
        isPanning: false
      });
      return true;
    }
  }, {
    key: "_onPanRotate",
    value: function _onPanRotate(event) {
      if (!this.dragRotate) {
        return false;
      }

      var pos = this.getCenter(event);
      var newMapState = this.mapState.rotate({
        pos: pos
      });
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isRotating: true
      });
      return true;
    }
  }, {
    key: "_onPanRotateEnd",
    value: function _onPanRotateEnd(event) {
      if (this.dragRotate) {
        var _this$dragRotate$iner = this.dragRotate.inertia,
            inertia = _this$dragRotate$iner === void 0 ? DEFAULT_INERTIA : _this$dragRotate$iner;

        if (inertia && event.velocity) {
          var pos = this.getCenter(event);
          var endPos = [pos[0] + event.velocityX * inertia / 2, pos[1] + event.velocityY * inertia / 2];
          var newControllerState = this.mapState.rotate({
            pos: endPos
          }).rotateEnd();
          this.updateViewport(newControllerState, _objectSpread(_objectSpread({}, LINEAR_TRANSITION_PROPS), {}, {
            transitionDuration: inertia,
            transitionEasing: INERTIA_EASING
          }), {
            isDragging: false,
            isRotating: true
          });
          return true;
        }
      }

      var newMapState = this.mapState.panEnd();
      this.updateViewport(newMapState, null, {
        isDragging: false,
        isRotating: false
      });
      return true;
    }
  }, {
    key: "_onWheel",
    value: function _onWheel(event) {
      if (!this.scrollZoom) {
        return false;
      }

      var _this$scrollZoom = this.scrollZoom,
          _this$scrollZoom$spee = _this$scrollZoom.speed,
          speed = _this$scrollZoom$spee === void 0 ? 0.01 : _this$scrollZoom$spee,
          _this$scrollZoom$smoo = _this$scrollZoom.smooth,
          smooth = _this$scrollZoom$smoo === void 0 ? false : _this$scrollZoom$smoo;
      event.preventDefault();
      var pos = this.getCenter(event);
      var delta = event.delta;
      var scale = 2 / (1 + Math.exp(-Math.abs(delta * speed)));

      if (delta < 0 && scale !== 0) {
        scale = 1 / scale;
      }

      var newMapState = this.mapState.zoom({
        pos: pos,
        scale: scale
      });

      if (newMapState.getViewportProps().zoom === this.mapStateProps.zoom) {
        return false;
      }

      this.updateViewport(newMapState, _objectSpread(_objectSpread({}, LINEAR_TRANSITION_PROPS), {}, {
        transitionInterpolator: new LinearInterpolator({
          around: pos
        }),
        transitionDuration: smooth ? 250 : 1
      }), {
        isPanning: true,
        isZooming: true
      });
      return true;
    }
  }, {
    key: "_onPinchStart",
    value: function _onPinchStart(event) {
      var pos = this.getCenter(event);
      var newMapState = this.mapState.zoomStart({
        pos: pos
      }).rotateStart({
        pos: pos
      });
      this._startPinchRotation = event.rotation;
      this._lastPinchEvent = event;
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isDragging: true
      });
      return true;
    }
  }, {
    key: "_onPinch",
    value: function _onPinch(event) {
      if (!this.isDragging()) {
        return false;
      }

      if (!this.touchZoom && !this.touchRotate) {
        return false;
      }

      var newMapState = this.mapState;

      if (this.touchZoom) {
        var scale = event.scale;
        var pos = this.getCenter(event);
        newMapState = newMapState.zoom({
          pos: pos,
          scale: scale
        });
      }

      if (this.touchRotate) {
        var rotation = event.rotation;
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
  }, {
    key: "_onPinchEnd",
    value: function _onPinchEnd(event) {
      if (!this.isDragging()) {
        return false;
      }

      if (this.touchZoom) {
        var _this$touchZoom$inert = this.touchZoom.inertia,
            inertia = _this$touchZoom$inert === void 0 ? DEFAULT_INERTIA : _this$touchZoom$inert;
        var _lastPinchEvent = this._lastPinchEvent;

        if (inertia && _lastPinchEvent && event.scale !== _lastPinchEvent.scale) {
          var pos = this.getCenter(event);

          var _newMapState = this.mapState.rotateEnd();

          var z = Math.log2(event.scale);

          var velocityZ = (z - Math.log2(_lastPinchEvent.scale)) / (event.deltaTime - _lastPinchEvent.deltaTime);

          var endScale = Math.pow(2, z + velocityZ * inertia / 2);
          _newMapState = _newMapState.zoom({
            pos: pos,
            scale: endScale
          }).zoomEnd();
          this.updateViewport(_newMapState, _objectSpread(_objectSpread({}, LINEAR_TRANSITION_PROPS), {}, {
            transitionInterpolator: new LinearInterpolator({
              around: pos
            }),
            transitionDuration: inertia,
            transitionEasing: INERTIA_EASING
          }), {
            isDragging: false,
            isPanning: Boolean(this.touchZoom),
            isZooming: Boolean(this.touchZoom),
            isRotating: false
          });
          this.blockEvents(inertia);
          return true;
        }
      }

      var newMapState = this.mapState.zoomEnd().rotateEnd();
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
  }, {
    key: "_onTriplePanStart",
    value: function _onTriplePanStart(event) {
      var pos = this.getCenter(event);
      var newMapState = this.mapState.rotateStart({
        pos: pos
      });
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isDragging: true
      });
      return true;
    }
  }, {
    key: "_onTriplePan",
    value: function _onTriplePan(event) {
      if (!this.isDragging()) {
        return false;
      }

      if (!this.touchRotate) {
        return false;
      }

      var pos = this.getCenter(event);
      pos[0] -= event.deltaX;
      var newMapState = this.mapState.rotate({
        pos: pos
      });
      this.updateViewport(newMapState, NO_TRANSITION_PROPS, {
        isRotating: true
      });
      return true;
    }
  }, {
    key: "_onTriplePanEnd",
    value: function _onTriplePanEnd(event) {
      if (!this.isDragging()) {
        return false;
      }

      if (this.touchRotate) {
        var _this$touchRotate$ine = this.touchRotate.inertia,
            inertia = _this$touchRotate$ine === void 0 ? DEFAULT_INERTIA : _this$touchRotate$ine;

        if (inertia && event.velocityY) {
          var pos = this.getCenter(event);
          var endPos = [pos[0], pos[1] += event.velocityY * inertia / 2];

          var _newMapState2 = this.mapState.rotate({
            pos: endPos
          });

          this.updateViewport(_newMapState2, _objectSpread(_objectSpread({}, LINEAR_TRANSITION_PROPS), {}, {
            transitionDuration: inertia,
            transitionEasing: INERTIA_EASING
          }), {
            isDragging: false,
            isRotating: true
          });
          this.blockEvents(inertia);
          return false;
        }
      }

      var newMapState = this.mapState.rotateEnd();
      this.updateViewport(newMapState, null, {
        isDragging: false,
        isRotating: false
      });
      return true;
    }
  }, {
    key: "_onDoubleTap",
    value: function _onDoubleTap(event) {
      if (!this.doubleClickZoom) {
        return false;
      }

      var pos = this.getCenter(event);
      var isZoomOut = this.isFunctionKeyPressed(event);
      var newMapState = this.mapState.zoom({
        pos: pos,
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
  }, {
    key: "_onKeyDown",
    value: function _onKeyDown(event) {
      if (!this.keyboard) {
        return false;
      }

      var funcKey = this.isFunctionKeyPressed(event);
      var _this$keyboard = this.keyboard,
          _this$keyboard$zoomSp = _this$keyboard.zoomSpeed,
          zoomSpeed = _this$keyboard$zoomSp === void 0 ? 2 : _this$keyboard$zoomSp,
          _this$keyboard$moveSp = _this$keyboard.moveSpeed,
          moveSpeed = _this$keyboard$moveSp === void 0 ? 100 : _this$keyboard$moveSp,
          _this$keyboard$rotate = _this$keyboard.rotateSpeedX,
          rotateSpeedX = _this$keyboard$rotate === void 0 ? 15 : _this$keyboard$rotate,
          _this$keyboard$rotate2 = _this$keyboard.rotateSpeedY,
          rotateSpeedY = _this$keyboard$rotate2 === void 0 ? 10 : _this$keyboard$rotate2;
      var mapStateProps = this.mapStateProps;
      var newMapState;

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
  }]);

  return MapController;
}();

export { MapController as default };
//# sourceMappingURL=map-controller.js.map