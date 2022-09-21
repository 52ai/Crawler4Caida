import "./styles/main.less";
import { hot } from 'react-hot-loader/root';
import React from "react";
import GalaxyPage from "./galaxy/galaxyPage.jsx";

const App = () => {
  return (
    <GalaxyPage />
  );
};

export default hot(App);
