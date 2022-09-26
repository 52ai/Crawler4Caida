"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = void 0;

var _slicedToArray2 = _interopRequireDefault(require("@babel/runtime/helpers/slicedToArray"));

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime/helpers/defineProperty"));

var React = _interopRequireWildcard(require("react"));

var PropTypes = _interopRequireWildcard(require("prop-types"));

var _mapContext = _interopRequireDefault(require("./map-context"));

var _assert = _interopRequireDefault(require("../utils/assert"));

var _deepEqual = _interopRequireDefault(require("../utils/deep-equal"));

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { (0, _defineProperty2["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

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
  (0, _assert["default"])(props.id === prevProps.id, 'source id changed');
  (0, _assert["default"])(props.type === prevProps.type, 'source type changed');
  var changedKey = '';
  var changedKeyCount = 0;

  for (var key in props) {
    if (key !== 'children' && key !== 'id' && !(0, _deepEqual["default"])(prevProps[key], props[key])) {
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
  var context = (0, React.useContext)(_mapContext["default"]);
  var propsRef = (0, React.useRef)({
    id: props.id,
    type: props.type
  });

  var _useState = (0, React.useState)(0),
      _useState2 = (0, _slicedToArray2["default"])(_useState, 2),
      setStyleLoaded = _useState2[1];

  var id = (0, React.useMemo)(function () {
    return props.id || "jsx-source-".concat(sourceCounter++);
  }, []);
  var map = context.map;
  (0, React.useEffect)(function () {
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
    return child && (0, React.cloneElement)(child, {
      source: id
    });
  }) || null;
}

Source.propTypes = propTypes;
var _default = Source;
exports["default"] = _default;
//# sourceMappingURL=source.js.map