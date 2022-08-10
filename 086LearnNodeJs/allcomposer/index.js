/**
 * Finds all dependencies save them into `outputFileName`
 */
var Crawler = require("crawler");
var outputFileName = 'composer_packages.json';
var fs = require('fs');
var semver = require('semver');

// How many packages did we process so far?
var total = 0;
// All packages are stored here:
var results = [];
// For some reason crawler fails with out of memory exception if you try load
// all 60k requests. Crawling it in chunks, where each chunk is 3000 packages.
// We will still do only 10 concurrent requests below. The chunk size is only
// used for queueing.
var chunkSize = 3000;

var getAllPackages = require('./lib/getAllPackages');
console.log('Loading list of all packages...');
getAllPackages().then(crawlDependencies);

return; // We are done here.

function crawlDependencies(index) {
  console.log('Loaded ' + index.length + ' packages to query');

  var c = new Crawler({
    jQuery: false,
    maxConnections: 10,
    // This will be called for each crawled page
    callback: indexPackage,
  });

  c.on('drain', saveAndExit);

  queueChunk();

  function queueChunk() {
    if (!index.length) return;
    if (index.length < chunkSize) {
      console.log('Queueing last ' + index.length + ' packages');
      c.queue(index.splice(0, index.length));
    } else {
      console.log('Queueing next ' + chunkSize + ' packages');
      c.queue(index.splice(0, chunkSize));
    }
  }

  function indexPackage(error, result, done) {
    total += 1;
    if (total % 100 === 0) {
      console.log('Processed ' + total + ' packages');
    }
    if (total % chunkSize === 0) {
      queueChunk();
    }

    var url = getUrl(result);
    if (error) {
      console.log('!! Error: ' + error + '; ' + url);
      done();
      return;
    }
    var body;
    try {
      body = JSON.parse(result.body);
    } catch (e) {
      console.log('Could not parse json response: ' + result.body + '; ' + url);
      done();
      return;
    }

    processBody(body);
    done();

    function processBody(body) {
      if (body.package) {
        processPackage(body.package);
      } else if (body.packages) {
        for (var name in body.packages) {
          if (body.packages.hasOwnProperty(name)) {
            processVersion(body.packages[name]);
          }
        }
      } else {
        console.log('Something is wrong with body. No package or packages for ' + JSON.stringify(body));
      }
    }

    function processPackage(pkg) {
      var versions = pkg.versions;
      if (!versions) {
        console.log(result);
        console.log('Could not find versions for ' + url);
        return;
      }
      processVersion(versions);
    }

    function processVersion(versions) {
      var latest = versions['dev-master'] || findLatest(versions);

      if (latest) results.push(latest);
      else {
        console.log(result, versions);
        console.log('Could not find latest version for ' + url);
      }
    }
  }
}


function getUrl(response) {
  if (!response) return '';
  return response.uri;
}

function saveAndExit() {
  console.log('saving...');
  fs.writeFileSync(outputFileName, JSON.stringify(results), 'utf8');
  console.log('Done!');
  console.log('Saved ' + results.length + ' packages into ' + outputFileName);
  console.log('Now run layout algorithm using:');
  console.log(' node layout.js');
  process.exit(0);
}

function findLatest(versions) {
  var mostRecent = Object.keys(versions).sort(bySemver);
  return versions[mostRecent[0]];
}

function bySemver(x, y) {
  var xValid = semver.valid(x);
  var yValid = semver.valid(y);
  if (xValid && yValid) return semver.rcompare(x, y);
  if (xValid && !yValid) return 1;
  if (yValid && !xValid) return 1;
  return 0;
}
