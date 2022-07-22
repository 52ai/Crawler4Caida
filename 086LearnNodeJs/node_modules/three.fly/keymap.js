/**
 * Defines default key bindings for the controls
 */
module.exports = createKeyMap;

function createKeyMap() {
  return {
    87: { name: 'forward' }, // W
    83: { name: 'back'}, // S
    65: { name: 'left'}, // A
    68: { name: 'right'},// D
    82: { name: 'up'}, // R
    70: { name: 'down'}, // F
    38: { name: 'pitchUp'}, // up
    40: { name: 'pitchDown'}, // down
    37: { name: 'yawLeft'}, // left
    39: { name: 'yawRight'}, // right
    81: { name: 'rollLeft'}, // Q
    69: { name: 'rollRight'}, // E
  };
}
