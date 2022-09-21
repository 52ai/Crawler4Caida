import './LocaleSelector.less';
import React from "react";
import config from "../../config.js";
import intl from "react-intl-universal";

const SUPPORT_LOCALES = config.supportLocales;

class LocaleSelector extends React.Component {
  constructor() {
    super();
    this.onSelectLocale = this.onSelectLocale.bind(this);
  }

  render() {
    var currentLocale = intl.determineLocale({localStorageLocaleKey: 'lang'});

    return (
      <div className="locale-selector">
        <select onChange={this.onSelectLocale} defaultValue={currentLocale}>
          {SUPPORT_LOCALES.map((locale) => (
            <option key={locale.value} value={locale.value}>
              {locale.name}
            </option>
          ))}
        </select>
      </div>
    );
  }

  onSelectLocale(e) {
    let lang = e.target.value;
    window.localStorage.setItem('lang', lang);
    window.location.reload();
  };
}

export default LocaleSelector;
