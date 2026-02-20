// interaction.js — Hover highlight, click-to-fly-in, label tooltip.

import * as THREE from 'three';
import { highlightBody } from './bodies.js';

export function setupInteraction(ctx, meshMap) {
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  const meshes = Array.from(meshMap.values());

  let hoveredMesh = null;
  let flyTarget = null;
  let flyProgress = 0;
  let flyFrom = null;
  let flyTo = null;
  let flyLookAt = null;

  // Tooltip element
  const tooltip = document.getElementById('tooltip');

  function onPointerMove(event) {
    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(pointer, ctx.camera);
    const hits = raycaster.intersectObjects(meshes);

    if (hits.length > 0) {
      const mesh = hits[0].object;
      if (mesh !== hoveredMesh) {
        highlightBody(hoveredMesh, false);
        hoveredMesh = mesh;
        highlightBody(hoveredMesh, true);
        document.body.style.cursor = 'pointer';
      }
      // Show tooltip
      if (tooltip && mesh.userData.body) {
        tooltip.textContent = mesh.userData.body.label;
        tooltip.style.left = event.clientX + 12 + 'px';
        tooltip.style.top = event.clientY - 8 + 'px';
        tooltip.style.opacity = '1';
      }
    } else {
      if (hoveredMesh) {
        highlightBody(hoveredMesh, false);
        hoveredMesh = null;
        document.body.style.cursor = 'default';
      }
      if (tooltip) tooltip.style.opacity = '0';
    }
  }

  function onClick(event) {
    if (!hoveredMesh) return;

    const body = hoveredMesh.userData.body;
    const targetPos = hoveredMesh.position.clone();

    // Fly camera toward the clicked body
    flyFrom = ctx.camera.position.clone();
    flyLookAt = targetPos.clone();

    // Position camera at a comfortable viewing distance
    const dir = ctx.camera.position.clone().sub(targetPos).normalize();
    const viewDist = 4.0 + (body.mass || 0.5) * 3.0;
    flyTo = targetPos.clone().add(dir.multiplyScalar(viewDist));

    flyProgress = 0;
    flyTarget = targetPos;
    ctx.controls.enabled = false;
  }

  window.addEventListener('pointermove', onPointerMove);
  window.addEventListener('click', onClick);

  // Return the per-frame updater for fly animation
  return function onFrame() {
    if (flyTarget && flyProgress < 1) {
      flyProgress += 0.02;
      const t = easeInOut(Math.min(flyProgress, 1));

      ctx.camera.position.lerpVectors(flyFrom, flyTo, t);
      ctx.controls.target.lerp(flyLookAt, t * 0.1 + 0.02);

      if (flyProgress >= 1) {
        ctx.controls.target.copy(flyLookAt);
        ctx.controls.enabled = true;
        flyTarget = null;
      }
    }
  };
}

function easeInOut(t) {
  return t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(-2 * t + 2, 3) / 2;
}
