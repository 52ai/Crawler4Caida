import React from 'react';
import commonPackageTemplate from './commonPackageTemplate.jsx';

export default require('maco').template(goSearch, React);

function goSearch(props) {
  var model = props.model;

  var link = 'http://go-search.org/view?id=' + encodeURIComponent(model.name);
  var linkText = (typeof model.name === 'string') ? model.name.replace('github.com/', '') : model.name;

  return commonPackageTemplate(model, link, linkText);
}
