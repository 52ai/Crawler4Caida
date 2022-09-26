"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _extends2 = _interopRequireDefault(require("@babel/runtime/helpers/extends"));

var _classCallCheck2 = _interopRequireDefault(require("@babel/runtime/helpers/classCallCheck"));

var _createClass2 = _interopRequireDefault(require("@babel/runtime/helpers/createClass"));

var _assertThisInitialized2 = _interopRequireDefault(require("@babel/runtime/helpers/assertThisInitialized"));

var _inherits2 = _interopRequireDefault(require("@babel/runtime/helpers/inherits"));

var _possibleConstructorReturn2 = _interopRequireDefault(require("@babel/runtime/helpers/possibleConstructorReturn"));

var _getPrototypeOf2 = _interopRequireDefault(require("@babel/runtime/helpers/getPrototypeOf"));

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var React = _interopRequireWildcard(require("react"));

var _useMapControl2 = _interopRequireWildcard(require("./use-map-control"));

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = (0, _getPrototypeOf2["default"])(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = (0, _getPrototypeOf2["default"])(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return (0, _possibleConstructorReturn2["default"])(this, result); }; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

function Control(props) {
  var instance = props.instance;

  var _useMapControl = (0, _useMapControl2["default"])(props),
      context = _useMapControl.context,
      containerRef = _useMapControl.containerRef;

  instance._context = context;
  instance._containerRef = containerRef;
  return instance._render();
}

var BaseControl = function (_PureComponent) {
  (0, _inherits2["default"])(BaseControl, _PureComponent);

  var _super = _createSuper(BaseControl);

  function BaseControl() {
    var _this;

    (0, _classCallCheck2["default"])(this, BaseControl);

    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    _this = _super.call.apply(_super, [this].concat(args));
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_context", {});
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_containerRef", (0, React.createRef)());
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_onScroll", function (evt) {});
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_onDragStart", function (evt) {});
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_onDblClick", function (evt) {});
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_onClick", function (evt) {});
    (0, _defineProperty2["default"])((0, _assertThisInitialized2["default"])(_this), "_onPointerMove", function (evt) {});
    return _this;
  }

  (0, _createClass2["default"])(BaseControl, [{
    key: "_render",
    value: function _render() {
      throw new Error('_render() not implemented');
    }
  }, {
    key: "render",
    value: function render() {
      return React.createElement(Control, (0, _extends2["default"])({
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
}(React.PureComponent);

exports["default"] = BaseControl;
(0, _defineProperty2["default"])(BaseControl, "propTypes", _useMapControl2.mapControlPropTypes);
(0, _defineProperty2["default"])(BaseControl, "defaultProps", _useMapControl2.mapControlDefaultProps);
//# sourceMappingURL=base-control.js.map