// bodies.js — Create Three.js meshes for knowledge bodies.
// Each body is a glowing sphere. Size from mass, color from data.

import * as THREE from 'three';
import { KIND, BASE_RADIUS } from '../core/types.js';

// Create all body meshes and add to scene.
// Returns Map<id, THREE.Mesh> for interaction lookups.
export function createBodies(scene, bodies, positions) {
  const meshMap = new Map();

  for (const body of bodies) {
    const pos = positions.get(body.id);
    if (!pos) continue;

    const kind = body.kind || KIND.MOON;
    const radius = (BASE_RADIUS[kind] || 0.5) * (0.5 + body.mass * 0.5);
    const [r, g, b] = body.color || [0.5, 0.5, 0.5];
    const color = new THREE.Color(r, g, b);

    const geometry = new THREE.SphereGeometry(radius, 32, 24);
    const material = new THREE.MeshStandardMaterial({
      color,
      emissive: color,
      emissiveIntensity: kind === KIND.GALAXY_CENTER ? 1.5 : 0.6,
      roughness: 0.3,
      metalness: 0.1,
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(pos.x, pos.y, pos.z);
    mesh.userData = { bodyId: body.id, body, baseEmissive: material.emissiveIntensity };

    scene.add(mesh);

    // Point light for galaxy center and stars
    if (kind === KIND.GALAXY_CENTER || kind === KIND.STAR) {
      const light = new THREE.PointLight(color, kind === KIND.GALAXY_CENTER ? 3.0 : 0.5, 20);
      light.position.copy(mesh.position);
      scene.add(light);
    }

    meshMap.set(body.id, mesh);
  }

  return meshMap;
}

// Highlight a body (on hover)
export function highlightBody(mesh, active) {
  if (!mesh) return;
  const base = mesh.userData.baseEmissive;
  mesh.material.emissiveIntensity = active ? base * 2.5 : base;
}
