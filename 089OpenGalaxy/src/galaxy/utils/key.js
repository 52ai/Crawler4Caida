export default {
  isModifier,

  H: 72,
  L: 76,
  Space: 32,
  '/': 191,
  // SODA
  BackSpace: 8,
  Tab: 9,
  BackQuote: 192
};

function isModifier(e) {
  return e.altKey || e.ctrlKey || e.metaKey || e.shiftKey;
}
