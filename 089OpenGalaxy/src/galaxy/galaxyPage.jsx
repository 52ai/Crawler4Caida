import React from 'react';
import LoadingIndicator from './loadingIndicator.jsx';
import Scene from './scene.jsx';
import appEvents from './service/appEvents.js';
import request from './service/request.js';
import config from '../config.js';
import intl from 'react-intl-universal';


const SUPPORT_LOCALES = config.supportLocales;

class galaxyPage extends React.Component {
  constructor() {
    super();
    this.loadLocales = this.loadLocales.bind(this);
  }

  state = {
    localeInitDone: false
  };

  componentDidMount() {
    this.loadLocales();

    // This doesn't seem to belong here. The whole routing system is a mess
    // TODO: Come up with better routing
    this.loadGraphIfRouteChanged();
  }

  render() {
    if (!this.state.localeInitDone) return null;

    return (
      <div>
        <LoadingIndicator />
        <Scene />
      </div>
    );
  };

  loadGraphIfRouteChanged() {
    // var routeChanged = this.props.params.name !== currentPath;
    // if (routeChanged) {
    //   currentPath = this.props.params.name;
    //   appEvents.downloadGraphRequested.fire(currentPath);
    // }
    // appEvents.queryChanged.fire();

    appEvents.downloadGraphRequested.fire('open_galaxy');
    appEvents.queryChanged.fire();
  }

  loadLocales() {
    // 先从localStorage中查键"lang"
    // 如果没查到会以浏览器语言为准
    let currentLocale = intl.determineLocale({
      localStorageLocaleKey: "lang"
    });

    // 如果没找到，则默认为English
    // if (!_.find(SUPPORT_LOCALES, { value: currentLocale })) {
    //   currentLocale = "en-US";
    // }

    request(`public/locales/${currentLocale}.json`, { responseType: "json" })
      .then((data) => {
        // init 方法将根据 currentLocale 来加载当前语言环境的数据
        return intl.init({
          currentLocale,
          locales: {
            [currentLocale]: data,
          },
        });
      })
      .then(() => {
        // After loading CLDR locale data, start to render
        this.setState({ localeInitDone: true });
      });
  }
}

export default galaxyPage;
