// placement.js — Pure placement algorithms.
// Input: bodies + bonds + options → Output: Map<id, {x, y, z}>
// No Three.js. No side effects.

import { KIND, BASE_RADIUS, ORBITAL_DISTANCE, DEFAULT_OPTIONS } from './types.js';
import { indexBodies, findRoots, walkTree } from './graph.js';

// Main entry point: choose algorithm by name
export function place(bodies, bonds, options = {}) {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  if (opts.algorithm === 'force-directed') {
    return forceDirected(bodies, bonds, opts);
  }
  return orbital(bodies, bonds, opts);
}

// --- Orbital placement ---
// Children orbit their parent at golden-angle spacing with slight polar tilt.
function orbital(bodies, bonds, opts) {
  const positions = new Map();
  const index = indexBodies(bodies);
  const roots = findRoots(bodies);

  // Place each root at origin (typically just one galaxy center)
  for (const rootId of roots) {
    positions.set(rootId, { x: 0, y: 0, z: 0 });
    placeChildren(index, rootId, positions, opts, 0);
  }

  return positions;
}

function placeChildren(index, parentId, positions, opts, siblingOffset) {
  const parent = index.get(parentId);
  if (!parent || !parent.children) return;

  const parentPos = positions.get(parentId);
  const n = parent.children.length;

  for (let i = 0; i < n; i++) {
    const childId = parent.children[i];
    const child = index.get(childId);
    if (!child) continue;

    const kind = child.kind || KIND.MOON;
    const dist = (ORBITAL_DISTANCE[kind] || 4.0) * (0.8 + child.mass * 0.4);

    // Golden angle spiral with tilt
    const angle = (i + siblingOffset) * opts.goldenAngle;
    const tilt = (i / (n + 1) - 0.5) * opts.tiltRange * Math.PI;

    const x = parentPos.x + dist * Math.cos(angle) * Math.cos(tilt);
    const y = parentPos.y + dist * Math.sin(tilt);
    const z = parentPos.z + dist * Math.sin(angle) * Math.cos(tilt);

    positions.set(childId, { x, y, z });
    placeChildren(index, childId, positions, opts, i * 3);
  }
}

// --- Force-directed placement ---
// Spring forces from bonds, universal repulsion, iterative relaxation.
function forceDirected(bodies, bonds, opts) {
  const index = indexBodies(bodies);

  // Initialize positions randomly in a sphere
  const pos = new Map();
  const vel = new Map();
  for (const b of bodies) {
    const r = 10 * Math.cbrt(Math.random());
    const theta = Math.acos(2 * Math.random() - 1);
    const phi = 2 * Math.PI * Math.random();
    pos.set(b.id, {
      x: r * Math.sin(theta) * Math.cos(phi),
      y: r * Math.sin(theta) * Math.sin(phi),
      z: r * Math.cos(theta),
    });
    vel.set(b.id, { x: 0, y: 0, z: 0 });
  }

  // Pin galaxy center at origin
  const roots = findRoots(bodies);
  for (const rootId of roots) {
    pos.set(rootId, { x: 0, y: 0, z: 0 });
  }

  // Iterate
  for (let iter = 0; iter < opts.forceIterations; iter++) {
    const forces = new Map();
    for (const b of bodies) forces.set(b.id, { x: 0, y: 0, z: 0 });

    // Repulsion: all pairs
    for (let i = 0; i < bodies.length; i++) {
      for (let j = i + 1; j < bodies.length; j++) {
        const a = bodies[i], b = bodies[j];
        const pa = pos.get(a.id), pb = pos.get(b.id);
        const dx = pa.x - pb.x, dy = pa.y - pb.y, dz = pa.z - pb.z;
        const distSq = dx * dx + dy * dy + dz * dz + 0.01;
        const f = opts.repulsionStrength / distSq;
        const fa = forces.get(a.id), fb = forces.get(b.id);
        fa.x += f * dx; fa.y += f * dy; fa.z += f * dz;
        fb.x -= f * dx; fb.y -= f * dy; fb.z -= f * dz;
      }
    }

    // Attraction: bonds + parent-child edges
    const edges = [...bonds];
    for (const b of bodies) {
      if (b.children) {
        for (const c of b.children) {
          edges.push({ from: b.id, to: c, strength: 0.5 });
        }
      }
    }

    for (const edge of edges) {
      const pa = pos.get(edge.from), pb = pos.get(edge.to);
      if (!pa || !pb) continue;
      const dx = pb.x - pa.x, dy = pb.y - pa.y, dz = pb.z - pa.z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) + 0.01;
      const f = opts.attractionStrength * (edge.strength || 0.5) * dist;
      const fa = forces.get(edge.from), fb = forces.get(edge.to);
      if (fa) { fa.x += f * dx / dist; fa.y += f * dy / dist; fa.z += f * dz / dist; }
      if (fb) { fb.x -= f * dx / dist; fb.y -= f * dy / dist; fb.z -= f * dz / dist; }
    }

    // Apply forces
    for (const b of bodies) {
      if (roots.includes(b.id)) continue; // pin roots
      const v = vel.get(b.id), f = forces.get(b.id), p = pos.get(b.id);
      v.x = (v.x + f.x) * opts.damping;
      v.y = (v.y + f.y) * opts.damping;
      v.z = (v.z + f.z) * opts.damping;
      p.x += v.x;
      p.y += v.y;
      p.z += v.z;
    }
  }

  return pos;
}
