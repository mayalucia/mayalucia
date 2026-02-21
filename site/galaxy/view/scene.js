// scene.js — Three.js scene setup, camera, post-processing bloom, render loop.
// This is the effectful shell. Owns the WebGL context and animation frame.
// Scene-level config (background, camera, bloom) comes from the active theme.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

export function createScene(canvas, theme) {
  const defaults = theme.getSceneDefaults();

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(defaults.background);

  const [cx, cy, cz] = defaults.cameraPos;
  const camera = new THREE.PerspectiveCamera(
    60, window.innerWidth / window.innerHeight,
    defaults.cameraNear || 0.1,
    defaults.cameraFar || 500,
  );
  camera.position.set(cx, cy, cz);

  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = defaults.orbitMinDistance || 3;
  controls.maxDistance = defaults.orbitMaxDistance || 100;

  if (defaults.cameraTarget) {
    const [tx, ty, tz] = defaults.cameraTarget;
    controls.target.set(tx, ty, tz);
    camera.lookAt(tx, ty, tz);
  }

  // Post-processing: bloom (strength varies by theme)
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));

  const bloom = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    defaults.bloomStrength,
    defaults.bloomRadius,
    defaults.bloomThreshold,
  );
  composer.addPass(bloom);

  // Let the theme set up environment (lighting, background geometry, fog)
  theme.renderEnvironment(scene);

  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
  });

  return { renderer, scene, camera, controls, composer };
}

// Render loop — call each frame callback, then composite
export function startLoop(ctx, onFrame) {
  function animate() {
    requestAnimationFrame(animate);
    ctx.controls.update();
    if (onFrame) onFrame(ctx);
    ctx.composer.render();
  }
  animate();
}
