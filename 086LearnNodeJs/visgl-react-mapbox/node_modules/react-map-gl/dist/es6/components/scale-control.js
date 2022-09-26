import * as React from 'react';
import { useEffect, useState, useMemo } from 'react';
import * as PropTypes from 'prop-types';
import mapboxgl from '../utils/mapboxgl';
import useMapControl, { mapControlDefaultProps, mapControlPropTypes } from './use-map-control';
const propTypes = Object.assign({}, mapControlPropTypes, {
  className: PropTypes.string,
  style: PropTypes.object,
  maxWidth: PropTypes.number,
  unit: PropTypes.oneOf(['imperial', 'metric', 'nautical'])
});
const defaultProps = Object.assign({}, mapControlDefaultProps, {
  className: '',
  maxWidth: 100,
  unit: 'metric'
});

function ScaleControl(props) {
  const {
    context,
    containerRef
  } = useMapControl(props);
  const [mapboxScaleControl, createMapboxScaleControl] = useState(null);
  useEffect(() => {
    if (context.map) {
      const control = new mapboxgl.ScaleControl();
      control._map = context.map;
      control._container = containerRef.current;
      createMapboxScaleControl(control);
    }
  }, [context.map]);

  if (mapboxScaleControl) {
    mapboxScaleControl.options = props;

    mapboxScaleControl._onMove();
  }

  const style = useMemo(() => ({
    position: 'absolute',
    ...props.style
  }), [props.style]);
  return React.createElement("div", {
    style: style,
    className: props.className
  }, React.createElement("div", {
    ref: containerRef,
    className: "mapboxgl-ctrl mapboxgl-ctrl-scale"
  }));
}

ScaleControl.propTypes = propTypes;
ScaleControl.defaultProps = defaultProps;
export default React.memo(ScaleControl);
//# sourceMappingURL=scale-control.js.map