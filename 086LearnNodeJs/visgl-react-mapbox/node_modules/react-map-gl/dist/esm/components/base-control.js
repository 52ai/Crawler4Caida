import _extends from "@babel/runtime/helpers/esm/extends";
import _classCallCheck from "@babel/runtime/helpers/esm/classCallCheck";
import _createClass from "@babel/runtime/helpers/esm/createClass";
import _assertThisInitialized from "@babel/runtime/helpers/esm/assertThisInitialized";
import _inherits from "@babel/runtime/helpers/esm/inherits";
import _possibleConstructorReturn from "@babel/runtime/helpers/esm/possibleConstructorReturn";
import _getPrototypeOf from "@babel/runtime/helpers/esm/getPrototypeOf";
import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

import * as React from 'react';
import { PureComponent, createRef } from 'react';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';

function Control(props) {
  var instance = props.instance;

  var _useMapControl = useMapControl(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  instance._context = context;
  instance._containerRef = containerRef;
  return instance._render();
}

var BaseControl = function (_PureComponent) {
  _inherits(BaseControl, _PureComponent);

  var _super = _createSuper(BaseControl);

  function BaseControl() {
    var _this;

    _classCallCheck(this, BaseControl);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    _this = _super.call.apply(_super, [this].concat(args));

    _defineProperty(_assertThisInitialized(_this), "_context", {});

    _defineProperty(_assertThisInitialized(_this), "_containerRef", createRef());

    _defineProperty(_assertThisInitialized(_this), "_onScroll", function (evt) {});

    _defineProperty(_assertThisInitialized(_this), "_onDragStart", function (evt) {});

    _defineProperty(_assertThisInitialized(_this), "_onDblClick", function (evt) {});

    _defineProperty(_assertThisInitialized(_this), "_onClick", function (evt) {});

    _defineProperty(_assertThisInitialized(_this), "_onPointerMove", function (evt) {});

    return _this;
  }

  _createClass(BaseControl, [{
    key: "_render",
    value: function _render() {
      throw new Error('_render() not implemented');
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(Control, _extends({
        instance: this
      }, this.props, {
        onScroll: this._onScroll,
        onDragStart: this._onDragStart,
        onDblClick: this._onDblClick,
        onClick: this._onClick,
        onPointerMove: this._onPointerMove
      }));
    }
  }]);

  return BaseControl;
}(PureComponent);

_defineProperty(BaseControl, "propTypes", mapControlPropTypes);

_defineProperty(BaseControl, "defaultProps", mapControlDefaultProps);

export { BaseControl as default };
//# sourceMappingURL=base-control.js.map