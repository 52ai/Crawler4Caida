import { useEffect, useLayoutEffect } from 'react';
var useIsomorphicLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;
export default useIsomorphicLayoutEffect;
//# sourceMappingURL=use-isomorphic-layout-effect.js.map