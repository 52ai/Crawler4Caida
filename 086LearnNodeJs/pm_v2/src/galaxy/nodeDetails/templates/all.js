/**
 * TODO: I need something better than this. Manually changing template is
 * very inconvenient :(. Should it be defined with metadata?
 */
import npm from './npm.jsx';
import gosearch from './gosearch.jsx';
import bower from './bower.jsx';
import composer from './composer.jsx';
import rubygems from './rubygems.jsx';
import cran from './cran.jsx';
import brew from './brew.jsx';
import debian from './debian.jsx';
import fedora from './fedora.jsx';
import nuget from './nuget.jsx';
import python from './python.jsx';
import google from './google.jsx';

import github from './github.jsx';

import defaultTemplate from './default.jsx';

export default {
  npm: npm,
  gosearch: gosearch,
  bower: bower,
  composer: composer,
  rubygems: rubygems,
  github: github,
  cran: cran,
  brew: brew,
  debian: debian,
  fedora: fedora,
  nuget: nuget,
  python: python,
  'covid-lit': google,
  default: defaultTemplate
}
