"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.setPathPrefix = setPathPrefix;
exports.getPathPrefix = getPathPrefix;
exports.addAliases = addAliases;
exports.resolvePath = resolvePath;
var pathPrefix = '';
var fileAliases = {};

function setPathPrefix(prefix) {
  pathPrefix = prefix;
}

function getPathPrefix() {
  return pathPrefix;
}

function addAliases(aliases) {
  Object.assign(fileAliases, aliases);
}

function resolvePath(filename) {
  for (var alias in fileAliases) {
    if (filename.startsWith(alias)) {
      var replacement = fileAliases[alias];
      filename = filename.replace(alias, replacement);
    }
  }

  if (!filename.startsWith('http://') && !filename.startsWith('https://')) {
    filename = "".concat(pathPrefix).concat(filename);
  }

  return filename;
}
//# sourceMappingURL=file-aliases.js.map