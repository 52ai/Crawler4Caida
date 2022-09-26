import * as React from 'react';
import { useContext, useEffect, useMemo, useState, useRef } from 'react';
import { cloneElement } from 'react';
import * as PropTypes from 'prop-types';
import MapContext from './map-context';
import assert from '../utils/assert';
import deepEqual from '../utils/deep-equal';
const propTypes = {
  type: PropTypes.string.isRequired,
  id: PropTypes.string
};
let sourceCounter = 0;

function createSource(map, id, props) {
  if (map.style && map.style._loaded) {
    const options = { ...props
    };
    delete options.id;
    delete options.children;
    map.addSource(id, options);
    return map.getSource(id);
  }

  return null;
}

function updateSource(source, props, prevProps) {
  assert(props.id === prevProps.id, 'source id changed');
  assert(props.type === prevProps.type, 'source type changed');
  let changedKey = '';
  let changedKeyCount = 0;

  for (const key in props) {
    if (key !== 'children' && key !== 'id' && !deepEqual(prevProps[key], props[key])) {
      changedKey = key;
      changedKeyCount++;
    }
  }

  if (!changedKeyCount) {
    return;
  }

  const {
    type
  } = props;

  if (type === 'geojson') {
    source.setData(props.data);
  } else if (type === 'image') {
    source.updateImage({
      url: props.url,
      coordinates: props.coordinates
    });
  } else if ((type === 'canvas' || type === 'video') && changedKeyCount === 1 && changedKey === 'coordinates') {
    source.setCoordinates(props.coordinates);
  } else if (type === 'vector' && source.setUrl) {
    switch (changedKey) {
      case 'url':
        source.setUrl(props.url);
        break;

      case 'tiles':
        source.setTiles(props.tiles);
        break;

      default:
    }
  } else {
    console.warn("Unable to update <Source> prop: ".concat(changedKey));
  }
}

function Source(props) {
  const context = useContext(MapContext);
  const propsRef = useRef({
    id: props.id,
    type: props.type
  });
  const [, setStyleLoaded] = useState(0);
  const id = useMemo(() => props.id || "jsx-source-".concat(sourceCounter++), []);
  const {
    map
  } = context;
  useEffect(() => {
    if (map) {
      const forceUpdate = () => setStyleLoaded(version => version + 1);

      map.on('styledata', forceUpdate);
      return () => {
        map.off('styledata', forceUpdate);
        requestAnimationFrame(() => {
          if (map.style && map.style._loaded && map.getSource(id)) {
            map.removeSource(id);
          }
        });
      };
    }

    return undefined;
  }, [map, id]);
  let source = map && map.style && map.getSource(id);

  if (source) {
    updateSource(source, props, propsRef.current);
  } else {
    source = createSource(map, id, props);
  }

  propsRef.current = props;
  return source && React.Children.map(props.children, child => child && cloneElement(child, {
    source: id
  })) || null;
}

Source.propTypes = propTypes;
export default Source;
//# sourceMappingURL=source.js.map