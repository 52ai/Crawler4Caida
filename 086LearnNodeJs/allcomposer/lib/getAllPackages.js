var rp = require('request-promise');
var query = 'https://packagist.org/packages/';
var packagesList = 'https://packagist.org/packages/list.json';

module.exports = getPackages;

function getPackages() {
  return rp(packagesList)
    .then(convertToPackagesList)
    .catch(reportError);
}

function convertToPackagesList(res) {
  return JSON.parse(res).packageNames.map(toUrl);
}

function reportError(err) {
  console.error(err);
  throw err;
}

function toUrl(x) {
  return query + x + '.json';
}
