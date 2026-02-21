// theme.js — Theme interface contract.
//
// A theme is an object with three methods:
//
//   renderEnvironment(scene)
//     Set up background, lighting, atmosphere, and any ambient geometry.
//     Called once at scene creation.
//
//   renderBody(scene, body, position)  →  THREE.Object3D
//     Create the visual representation of a knowledge body.
//     Must set mesh.userData = { bodyId, body, baseEmissive }
//     for interaction.js compatibility.
//
//   renderBond(scene, bond, fromPos, toPos, fromBody, toBody)  →  THREE.Object3D
//     Create the visual connection between two bonded bodies.
//
//   highlightBody(mesh, active)
//     Visual feedback on hover. Toggle highlight state.
//
//   getSceneDefaults()  →  { background, cameraPos, bloomStrength, bloomRadius, bloomThreshold }
//     Scene-level configuration that varies per theme.

export function validateTheme(theme) {
  const required = ['renderEnvironment', 'renderBody', 'renderBond', 'highlightBody', 'getSceneDefaults'];
  for (const fn of required) {
    if (typeof theme[fn] !== 'function') {
      throw new Error(`Theme missing required method: ${fn}`);
    }
  }
  return theme;
}
