const refProps = ['type', 'source', 'source-layer', 'minzoom', 'maxzoom', 'filter', 'layout'];
export function normalizeStyle(style) {
  if (!style) {
    return null;
  }

  if (typeof style === 'string') {
    return style;
  }

  if (style.toJS) {
    style = style.toJS();
  }

  const layerIndex = {};

  for (const layer of style.layers) {
    layerIndex[layer.id] = layer;
  }

  const layers = style.layers.map(layer => {
    const layerRef = layerIndex[layer.ref];
    let normalizedLayer = null;

    if ('interactive' in layer) {
      normalizedLayer = { ...layer
      };
      delete normalizedLayer.interactive;
    }

    if (layerRef) {
      normalizedLayer = normalizedLayer || { ...layer
      };
      delete normalizedLayer.ref;

      for (const propName of refProps) {
        if (propName in layerRef) {
          normalizedLayer[propName] = layerRef[propName];
        }
      }
    }

    return normalizedLayer || layer;
  });
  return { ...style,
    layers
  };
}
//# sourceMappingURL=style-utils.js.map