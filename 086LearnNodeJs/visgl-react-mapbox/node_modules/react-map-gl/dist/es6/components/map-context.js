import * as React from 'react';
import { createContext, useState, useContext } from 'react';
const MapContext = createContext({
  viewport: null,
  map: null,
  container: null,
  onViewportChange: null,
  onViewStateChange: null,
  eventManager: null
});
export const MapContextProvider = MapContext.Provider;

function WrappedProvider({
  value,
  children
}) {
  const [map, setMap] = useState(null);
  const context = useContext(MapContext);
  value = {
    setMap,
    ...context,
    map: context && context.map || map,
    ...value
  };
  return React.createElement(MapContextProvider, {
    value: value
  }, children);
}

MapContext.Provider = WrappedProvider;
export default MapContext;
//# sourceMappingURL=map-context.js.map