export { VERSION } from '@probe.gl/env';
// ENVIRONMENT
export { self, window, global, document, process, console } from '@probe.gl/env';
export { isBrowser, isBrowserMainThread } from '@probe.gl/env';
export { getBrowser, isMobile } from '@probe.gl/env';
export { isElectron } from '@probe.gl/env';
// ENVIRONMENT'S ASSERT IS 5-15KB, SO WE PROVIDE OUR OWN
export { assert } from '@probe.gl/env';
// LOGGING
export { Log } from '@probe.gl/log';
export { COLOR } from '@probe.gl/log';
// DEFAULT EXPORT IS A LOG INSTANCE
export { default as default } from '@probe.gl/log';
// UTILITIES
export { addColor } from '@probe.gl/log';
export { leftPad, rightPad } from '@probe.gl/log';
export { autobind } from '@probe.gl/log';
export { default as LocalStorage } from '@probe.gl/log';
export { default as getHiResTimestamp } from '@probe.gl/log';
// DEPRECATED (Should be imported directly from @probe.gl/stats)
export { Stats, Stat } from '@probe.gl/stats';
