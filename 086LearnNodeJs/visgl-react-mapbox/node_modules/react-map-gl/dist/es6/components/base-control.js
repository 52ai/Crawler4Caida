import _extends from "@babel/runtime/helpers/esm/extends";
import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";
import * as React from 'react';
import { PureComponent, createRef } from 'react';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';

function Control(props) {
  const {
    instance
  } = props;
  const {
    context,
    containerRef
  } = useMapControl(props);
  instance._context = context;
  instance._containerRef = containerRef;
  return instance._render();
}

export default class BaseControl extends PureComponent {
  constructor(...args) {
    super(...args);

    _defineProperty(this, "_context", {});

    _defineProperty(this, "_containerRef", createRef());

    _defineProperty(this, "_onScroll", evt => {});

    _defineProperty(this, "_onDragStart", evt => {});

    _defineProperty(this, "_onDblClick", evt => {});

    _defineProperty(this, "_onClick", evt => {});

    _defineProperty(this, "_onPointerMove", evt => {});
  }

  _render() {
    throw new Error('_render() not implemented');
  }

  render() {
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

}

_defineProperty(BaseControl, "propTypes", mapControlPropTypes);

_defineProperty(BaseControl, "defaultProps", mapControlDefaultProps);
//# sourceMappingURL=base-control.js.map