import React from 'react';
import commonPackageTemplate from './commonPackageTemplate.jsx';

export default require('maco').template(bower, React);

function bower(props) {
  var model = props.model;

  var link = 'http://bower.io/search/?q=' + encodeURIComponent(model.name);
  var linkText = model.name;

  return commonPackageTemplate(model, link, linkText);
}
