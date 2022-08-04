"use strict";

var _typeof = require("@babel/runtime/helpers/typeof");

Object.defineProperty(exports, "__esModule", {
  value: true
});
Object.defineProperty(exports, "COLOR", {
  enumerable: true,
  get: function get() {
    return _log.COLOR;
  }
});
Object.defineProperty(exports, "LocalStorage", {
  enumerable: true,
  get: function get() {
    return _log.default;
  }
});
Object.defineProperty(exports, "Log", {
  enumerable: true,
  get: function get() {
    return _log.Log;
  }
});
Object.defineProperty(exports, "Stat", {
  enumerable: true,
  get: function get() {
    return _stats.Stat;
  }
});
Object.defineProperty(exports, "Stats", {
  enumerable: true,
  get: function get() {
    return _stats.Stats;
  }
});
Object.defineProperty(exports, "VERSION", {
  enumerable: true,
  get: function get() {
    return _env.VERSION;
  }
});
Object.defineProperty(exports, "addColor", {
  enumerable: true,
  get: function get() {
    return _log.addColor;
  }
});
Object.defineProperty(exports, "assert", {
  enumerable: true,
  get: function get() {
    return _env.assert;
  }
});
Object.defineProperty(exports, "autobind", {
  enumerable: true,
  get: function get() {
    return _log.autobind;
  }
});
Object.defineProperty(exports, "console", {
  enumerable: true,
  get: function get() {
    return _env.console;
  }
});
Object.defineProperty(exports, "default", {
  enumerable: true,
  get: function get() {
    return _log.default;
  }
});
Object.defineProperty(exports, "document", {
  enumerable: true,
  get: function get() {
    return _env.document;
  }
});
Object.defineProperty(exports, "getBrowser", {
  enumerable: true,
  get: function get() {
    return _env.getBrowser;
  }
});
Object.defineProperty(exports, "getHiResTimestamp", {
  enumerable: true,
  get: function get() {
    return _log.default;
  }
});
Object.defineProperty(exports, "global", {
  enumerable: true,
  get: function get() {
    return _env.global;
  }
});
Object.defineProperty(exports, "isBrowser", {
  enumerable: true,
  get: function get() {
    return _env.isBrowser;
  }
});
Object.defineProperty(exports, "isBrowserMainThread", {
  enumerable: true,
  get: function get() {
    return _env.isBrowserMainThread;
  }
});
Object.defineProperty(exports, "isElectron", {
  enumerable: true,
  get: function get() {
    return _env.isElectron;
  }
});
Object.defineProperty(exports, "isMobile", {
  enumerable: true,
  get: function get() {
    return _env.isMobile;
  }
});
Object.defineProperty(exports, "leftPad", {
  enumerable: true,
  get: function get() {
    return _log.leftPad;
  }
});
Object.defineProperty(exports, "process", {
  enumerable: true,
  get: function get() {
    return _env.process;
  }
});
Object.defineProperty(exports, "rightPad", {
  enumerable: true,
  get: function get() {
    return _log.rightPad;
  }
});
Object.defineProperty(exports, "self", {
  enumerable: true,
  get: function get() {
    return _env.self;
  }
});
Object.defineProperty(exports, "window", {
  enumerable: true,
  get: function get() {
    return _env.window;
  }
});

var _env = require("@probe.gl/env");

var _log = _interopRequireWildcard(require("@probe.gl/log"));

var _stats = require("@probe.gl/stats");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }
//# sourceMappingURL=index.js.map