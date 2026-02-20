// connections.js — Render bonds between bodies as luminous lines.

import * as THREE from 'three';

// Create line segments for all bonds. Returns the Group for cleanup.
export function createConnections(scene, bonds, positions, bodyIndex) {
  const group = new THREE.Group();

  for (const bond of bonds) {
    const from = positions.get(bond.from);
    const to = positions.get(bond.to);
    if (!from || !to) continue;

    const fromBody = bodyIndex.get(bond.from);
    const toBody = bodyIndex.get(bond.to);

    // Blend colors from the two connected bodies
    const fromColor = fromBody ? fromBody.color || [0.5, 0.5, 0.5] : [0.5, 0.5, 0.5];
    const toColor = toBody ? toBody.color || [0.5, 0.5, 0.5] : [0.5, 0.5, 0.5];

    const geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(from.x, from.y, from.z),
      new THREE.Vector3(to.x, to.y, to.z),
    ]);

    // Vertex colors for gradient effect
    const colors = new Float32Array([
      ...fromColor, ...toColor,
    ]);
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.15 + (bond.strength || 0.5) * 0.35,
      linewidth: 1,
    });

    group.add(new THREE.Line(geometry, material));
  }

  scene.add(group);
  return group;
}
