import _slicedToArray from "@babel/runtime/helpers/esm/slicedToArray";
import _defineProperty from "@babel/runtime/helpers/esm/defineProperty";

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

import * as React from 'react';
import { useContext, useEffect, useMemo, useState, useRef } from 'react';
import { cloneElement } from 'react';
import * as PropTypes from 'prop-types';
import MapContext from './map-context';
import assert from '../utils/assert';
import deepEqual from '../utils/deep-equal';
var propTypes = {
  type: PropTypes.string.isRequired,
  id: PropTypes.string
};
var sourceCounter = 0;

function createSource(map, id, props) {
  if (map.style && map.style._loaded) {
    var options = _objectSpread({}, props);

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
  var changedKey = '';
  var changedKeyCount = 0;

  for (var key in props) {
    if (key !== 'children' && key !== 'id' && !deepEqual(prevProps[key], props[key])) {
      changedKey = key;
      changedKeyCount++;
    }
  }

  if (!changedKeyCount) {
    return;
  }

  var type = props.type;

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
  var context = useContext(MapContext);
  var propsRef = useRef({
    id: props.id,
    type: props.type
  });

  var _useState = useState(0),
      _useState2 = _slicedToArray(_useState, 2),
      setStyleLoaded = _useState2[1];

  var id = useMemo(function () {
    return props.id || "jsx-source-".concat(sourceCounter++);
  }, []);
  var map = context.map;
  useEffect(function () {
    if (map) {
      var forceUpdate = function forceUpdate() {
        return setStyleLoaded(function (version) {
          return version + 1;
        });
      };

      map.on('styledata', forceUpdate);
      return function () {
        map.off('styledata', forceUpdate);
        requestAnimationFrame(function () {
          if (map.style && map.style._loaded && map.getSource(id)) {
            map.removeSource(id);
          }
        });
      };
    }

    return undefined;
  }, [map, id]);
  var source = map && map.style && map.getSource(id);

  if (source) {
    updateSource(source, props, propsRef.current);
  } else {
    source = createSource(map, id, props);
  }

  propsRef.current = props;
  return source && React.Children.map(props.children, function (child) {
    return child && cloneElement(child, {
      source: id
    });
  }) || null;
}

Source.propTypes = propTypes;
export default Source;
//# sourceMappingURL=source.js.map