// tree.js — Banj oak (Quercus leucotrichophora) theme.
//
// MāyāLucIA as a Himalayan oak: gnarled trunk, spreading crown,
// moss-draped branches twisting toward light. Each branch is a module,
// each leaf cluster a subproject. Cross-connections are moss trails
// and lichens bridging branches.
//
// The banj never grows straight. Every fork is a decision, every bend
// a response to wind, light, the weight of snow. Like a project.

import * as THREE from 'three';
import { KIND } from '../../core/types.js';

// ─── Seeded RNG ──────────────────────────────────────────────────────────────

function seededRNG(seed) {
  let s = seed | 0 || 1;
  return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}

function hashStr(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  return Math.abs(h) || 1;
}

// ─── Tree geometry generation ────────────────────────────────────────────────

// A branch segment: start point, end point, radius, children
// We build the tree recursively from the knowledge graph.

const TRUNK_RADIUS = 0.5;
const TRUNK_HEIGHT = 3.0;
const BRANCH_TAPER = 0.68;       // radius multiplies by this at each fork
const BRANCH_LENGTH_BASE = 2.2;  // shorter, denser branching
const BRANCH_LENGTH_TAPER = 0.65;
const BRANCH_DROOP = -0.10;      // banj branches droop slightly
const BRANCH_TWIST = 0.55;       // how much branches twist (radians range)
const SEGMENTS_PER_BRANCH = 6;
const RADIAL_SEGMENTS = 8;

// Bark color — grey-brown, rough, with lichen patches
const BARK_COLOR = 0x5A4A3A;
const BARK_LICHEN = 0x6A7A5A;

// ─── Module state ────────────────────────────────────────────────────────────

let branchEndpoints = new Map();  // bodyId → { position, direction, radius }
let leafGroups = new Map();       // bodyId → THREE.Group

// ─── Theme export ────────────────────────────────────────────────────────────

export default {
  getSceneDefaults() {
    return {
      background: 0xD8DDE3,           // overcast Himalayan sky
      cameraPos: [4, 5, 8],           // closer, portrait framing
      cameraTarget: [0, 4, 0],
      cameraNear: 0.1,
      cameraFar: 200,
      orbitMinDistance: 2,
      orbitMaxDistance: 30,
      bloomStrength: 0.08,
      bloomRadius: 0.5,
      bloomThreshold: 0.9,
    };
  },

  renderEnvironment(scene) {
    branchEndpoints = new Map();
    leafGroups = new Map();

    // Soft forest light — filtered through canopy
    scene.add(new THREE.HemisphereLight(0xA0B0A8, 0x3A4030, 0.6));

    // Dappled sunlight from above-left
    const sun = new THREE.DirectionalLight(0xFFF0D8, 0.7);
    sun.position.set(5, 12, 3);
    scene.add(sun);

    // Cool fill
    const fill = new THREE.DirectionalLight(0x90A0B0, 0.2);
    fill.position.set(-4, 6, -3);
    scene.add(fill);

    scene.add(new THREE.AmbientLight(0x506050, 0.15));

    // Gentle fog — forest atmosphere
    scene.fog = new THREE.FogExp2(0xD0D8DD, 0.018);

    buildGround(scene);
    buildSkyDome(scene);
  },

  renderBody(scene, body, position) {
    // Bodies are rendered as part of the tree in generateTerrain.
    // Here we just create invisible markers for interaction.
    const kind = body.kind || KIND.MOON;
    const markerR =
      kind === KIND.GALAXY_CENTER ? 1.2 :
      kind === KIND.STAR ? 0.6 :
      kind === KIND.PLANET ? 0.4 : 0.25;

    const markerGeo = new THREE.SphereGeometry(markerR, 8, 6);
    const markerMat = new THREE.MeshBasicMaterial({
      transparent: true, opacity: 0, depthWrite: false,
    });
    const marker = new THREE.Mesh(markerGeo, markerMat);
    marker.position.set(0, 0, 0); // repositioned in generateTerrain
    marker.userData = { bodyId: body.id, body, baseEmissive: 0 };
    scene.add(marker);
    return marker;
  },

  renderBond(scene, bond, fromPos, toPos) {
    // Bonds rendered as moss/lichen trails in generateTerrain
    if (!this._bonds) this._bonds = [];
    this._bonds.push(bond);
    const geo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(), new THREE.Vector3(),
    ]);
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ visible: false }));
    scene.add(line);
    return line;
  },

  highlightBody(mesh, active) {
    if (!mesh?.userData?.body) return;
    const id = mesh.userData.body.id;
    const leaves = leafGroups.get(id);
    if (leaves) {
      leaves.traverse(child => {
        if (child.isMesh && child.material) {
          if (active) {
            child.material.emissiveIntensity = 0.4;
          } else {
            child.material.emissiveIntensity = child.userData?.baseEmissive || 0.05;
          }
        }
      });
    }
    // Glow the marker slightly
    if (mesh.material) {
      mesh.material.opacity = active ? 0.15 : 0;
      mesh.material.color = active
        ? new THREE.Color(1, 0.9, 0.5)
        : new THREE.Color(1, 1, 1);
    }
  },

  async generateTerrain(scene, camera, controls) {
    // Build the oak from the knowledge graph
    // We need the bodies — collect them from scene userData markers
    const bodies = [];
    const bodyMap = new Map();
    scene.traverse(obj => {
      if (obj.userData?.body) {
        bodies.push(obj.userData.body);
        bodyMap.set(obj.userData.body.id, obj);
      }
    });

    // Find root
    const root = bodies.find(b => b.kind === KIND.GALAXY_CENTER);
    if (!root) return;

    // Build parent→children map
    const childrenOf = new Map();
    for (const b of bodies) {
      if (b.children) childrenOf.set(b.id, b.children);
    }

    // Grow the tree
    const rng = seededRNG(31415);
    const trunkBase = new THREE.Vector3(0, 0, 0);
    const trunkTop = new THREE.Vector3(0, TRUNK_HEIGHT, 0);

    // Draw trunk
    buildBranchSegment(scene, trunkBase, trunkTop, TRUNK_RADIUS, TRUNK_RADIUS * 0.7, rng);

    // Register trunk endpoint for root body
    branchEndpoints.set(root.id, {
      position: trunkTop.clone(),
      direction: new THREE.Vector3(0, 1, 0),
      radius: TRUNK_RADIUS * 0.7,
    });

    // Build root leaves (crown at trunk top)
    const rootLeaves = buildLeafCluster(scene, trunkTop, 1.5, root.color, rng);
    leafGroups.set(root.id, rootLeaves);

    // Position root marker
    const rootMarker = bodyMap.get(root.id);
    if (rootMarker) rootMarker.position.copy(trunkTop);

    // Grow main branches for star/planet children
    const children = childrenOf.get(root.id) || [];
    const nBranches = children.length;
    const goldenAngle = 2.39996;

    for (let i = 0; i < nBranches; i++) {
      const childId = children[i];
      const childBody = bodies.find(b => b.id === childId);
      if (!childBody) continue;

      const isStar = childBody.kind === KIND.STAR;
      const branchLen = isStar
        ? BRANCH_LENGTH_BASE + (rng() - 0.3) * 1.2
        : BRANCH_LENGTH_BASE * 0.7 + (rng() - 0.3) * 0.8;
      const branchR = isStar
        ? TRUNK_RADIUS * BRANCH_TAPER
        : TRUNK_RADIUS * BRANCH_TAPER * 0.7;

      // Spread branches around the trunk using golden angle
      const azimuth = i * goldenAngle + rng() * 0.3;
      // Elevation: banj branches spread wide, slight upward tendency
      const elevation = 0.2 + rng() * 0.5; // 0.2-0.7 radians from horizontal

      const dir = new THREE.Vector3(
        Math.cos(azimuth) * Math.cos(elevation),
        Math.sin(elevation) + BRANCH_DROOP,
        Math.sin(azimuth) * Math.cos(elevation),
      ).normalize();

      // Banj branches are never straight — add intermediate waypoints
      const branchEnd = growBranch(
        scene, trunkTop, dir, branchLen, branchR, rng, childBody.color
      );

      branchEndpoints.set(childId, {
        position: branchEnd.clone(),
        direction: dir.clone(),
        radius: branchR * BRANCH_TAPER,
      });

      // Leaf cluster at branch end — generous, full canopy
      const leafSize = isStar ? 2.0 : 1.4;
      const leaves = buildLeafCluster(scene, branchEnd, leafSize, childBody.color, rng);
      leafGroups.set(childId, leaves);

      // Position marker
      const marker = bodyMap.get(childId);
      if (marker) marker.position.copy(branchEnd);

      // Sub-branches for this body's children (moons)
      const subChildren = childrenOf.get(childId) || [];
      for (let j = 0; j < subChildren.length; j++) {
        const subId = subChildren[j];
        const subBody = bodies.find(b => b.id === subId);
        if (!subBody) continue;

        const subLen = branchLen * BRANCH_LENGTH_TAPER + (rng() - 0.3) * 0.5;
        const subR = branchR * BRANCH_TAPER;

        const subAzimuth = azimuth + (j - (subChildren.length - 1) / 2) * 0.8 + rng() * 0.3;
        const subElev = elevation * 0.5 + rng() * 0.4;

        const subDir = new THREE.Vector3(
          Math.cos(subAzimuth) * Math.cos(subElev),
          Math.sin(subElev) + BRANCH_DROOP * 1.5,
          Math.sin(subAzimuth) * Math.cos(subElev),
        ).normalize();

        const subEnd = growBranch(
          scene, branchEnd, subDir, subLen, subR, rng, subBody.color
        );

        branchEndpoints.set(subId, {
          position: subEnd.clone(),
          direction: subDir.clone(),
          radius: subR * BRANCH_TAPER,
        });

        const subLeaves = buildLeafCluster(scene, subEnd, 1.1, subBody.color, rng);
        leafGroups.set(subId, subLeaves);

        const subMarker = bodyMap.get(subId);
        if (subMarker) subMarker.position.copy(subEnd);
      }
    }

    // Filler branches — thicken the canopy with unnamed twigs and leaf masses
    buildFillerBranches(scene, trunkTop, nBranches, rng);

    // Bonds — moss/lichen trails between branches
    for (const bond of (this._bonds || [])) {
      const fromEp = branchEndpoints.get(bond.from);
      const toEp = branchEndpoints.get(bond.to);
      if (fromEp && toEp) {
        buildMossTrail(scene, fromEp.position, toEp.position, bond.strength || 0.5, rng);
      }
    }

    // Hanging moss from larger branches
    buildHangingMoss(scene, rng);

    // Roots at base
    buildRoots(scene, rng);

    // Reposition camera
    if (camera && controls) {
      controls.target.set(0, TRUNK_HEIGHT + 1, 0);
      camera.position.set(8, TRUNK_HEIGHT + 3, 10);
      camera.lookAt(0, TRUNK_HEIGHT + 1, 0);
      controls.update();
    }
  },
};

// ─── Branch growing ──────────────────────────────────────────────────────────

function growBranch(scene, start, direction, length, startRadius, rng, color) {
  // Banj branches curve and twist — build as a series of short segments
  const nSegs = 3 + Math.floor(length);
  const segLen = length / nSegs;
  let pos = start.clone();
  let dir = direction.clone().normalize();
  let radius = startRadius;

  for (let i = 0; i < nSegs; i++) {
    // Perturb direction — the banj twist
    const twist = new THREE.Vector3(
      (rng() - 0.5) * BRANCH_TWIST,
      (rng() - 0.3) * 0.3,        // slight upward bias
      (rng() - 0.5) * BRANCH_TWIST,
    );
    dir.add(twist).normalize();

    const endRadius = radius * (0.8 + rng() * 0.1);
    const end = pos.clone().add(dir.clone().multiplyScalar(segLen));

    buildBranchSegment(scene, pos, end, radius, endRadius, rng);

    pos = end;
    radius = endRadius;
  }

  return pos;
}

function buildBranchSegment(scene, start, end, startR, endR, rng) {
  const direction = end.clone().sub(start);
  const length = direction.length();
  if (length < 0.01) return;

  // Use a tapered cylinder (CylinderGeometry with different top/bottom radii)
  const geo = new THREE.CylinderGeometry(endR, startR, length, RADIAL_SEGMENTS, 1);

  // Bark material with subtle variation
  const barkHue = rng() > 0.7 ? BARK_LICHEN : BARK_COLOR;
  const mat = new THREE.MeshStandardMaterial({
    color: barkHue,
    roughness: 0.95,
    metalness: 0.0,
    flatShading: true,
  });

  const mesh = new THREE.Mesh(geo, mat);

  // Position: midpoint between start and end
  const mid = start.clone().add(end).multiplyScalar(0.5);
  mesh.position.copy(mid);

  // Orient cylinder to align with direction
  const up = new THREE.Vector3(0, 1, 0);
  const quat = new THREE.Quaternion().setFromUnitVectors(up, direction.normalize());
  mesh.quaternion.copy(quat);

  scene.add(mesh);
}

// ─── Filler branches (unnamed, thicken the canopy) ───────────────────────────

function buildFillerBranches(scene, trunkTop, existingBranches, rng) {
  // Add extra small branches between the named ones to fill out the crown.
  // A real banj has dozens of branches — the knowledge graph only gives us 7.
  const nFiller = 10 + Math.floor(rng() * 6);
  const goldenAngle = 2.39996;
  const baseColor = [0.15, 0.30, 0.10];

  for (let i = 0; i < nFiller; i++) {
    const azimuth = (existingBranches + i) * goldenAngle + rng() * 0.5;
    const elevation = 0.15 + rng() * 0.65;
    const len = 1.2 + rng() * 1.8;
    const radius = 0.05 + rng() * 0.08;

    // Some sprout from trunk top, some from partway up
    const startY = TRUNK_HEIGHT * (0.5 + rng() * 0.5);
    const start = new THREE.Vector3(
      Math.cos(azimuth) * TRUNK_RADIUS * 0.4,
      startY,
      Math.sin(azimuth) * TRUNK_RADIUS * 0.4,
    );

    const dir = new THREE.Vector3(
      Math.cos(azimuth) * Math.cos(elevation),
      Math.sin(elevation) + BRANCH_DROOP,
      Math.sin(azimuth) * Math.cos(elevation),
    ).normalize();

    const end = growBranch(scene, start, dir, len, radius, rng, baseColor);

    // Small leaf cluster at the tip
    const leafSize = 0.6 + rng() * 0.8;
    // Slightly vary the green
    const tintedColor = [
      0.10 + rng() * 0.08,
      0.25 + rng() * 0.15,
      0.06 + rng() * 0.06,
    ];
    buildLeafCluster(scene, end, leafSize, tintedColor, rng);
  }
}

// ─── Leaf clusters ───────────────────────────────────────────────────────────

function buildLeafCluster(scene, center, size, bodyColor, rng) {
  const group = new THREE.Group();

  const [cr, cg, cb] = bodyColor || [0.3, 0.6, 0.2];
  // Banj oak leaves: dark green with the body's colour as a tint
  const baseGreen = new THREE.Color(0.08, 0.22, 0.06);
  const tint = new THREE.Color(cr, cg, cb);
  const leafColor = baseGreen.clone().lerp(tint, 0.25);

  const nLeaves = Math.floor(15 + size * 18);
  const leafGeo = new THREE.SphereGeometry(1, 5, 4);

  for (let i = 0; i < nLeaves; i++) {
    // Scatter leaves in a rough sphere around the branch tip
    const theta = rng() * Math.PI * 2;
    const phi = rng() * Math.PI;
    const r = size * (0.3 + rng() * 0.7);

    const x = center.x + r * Math.sin(phi) * Math.cos(theta);
    const y = center.y + r * Math.sin(phi) * Math.sin(theta) * 0.6 + size * 0.2; // slightly flattened, lifted
    const z = center.z + r * Math.cos(phi);

    const leafScale = size * (0.14 + rng() * 0.14);

    // Vary leaf colour
    const lc = leafColor.clone();
    lc.r += (rng() - 0.5) * 0.04;
    lc.g += (rng() - 0.5) * 0.06;
    lc.b += (rng() - 0.5) * 0.03;

    const mat = new THREE.MeshStandardMaterial({
      color: lc,
      emissive: tint,
      emissiveIntensity: 0.05,
      roughness: 0.75,
      flatShading: true,
      transparent: true,
      opacity: 0.90 + rng() * 0.10,
    });

    const leaf = new THREE.Mesh(leafGeo, mat);
    leaf.position.set(x, y, z);
    leaf.scale.set(leafScale, leafScale * 0.5, leafScale * 0.8);
    leaf.rotation.set(rng() * Math.PI, rng() * Math.PI, rng() * 0.5);
    leaf.userData = { baseEmissive: 0.05 };

    group.add(leaf);
  }

  scene.add(group);
  return group;
}

// ─── Moss trails (bonds between branches) ────────────────────────────────────

function buildMossTrail(scene, from, to, strength, rng) {
  // A thin, slightly sagging curve of moss between two branch endpoints
  const mid = from.clone().add(to).multiplyScalar(0.5);
  mid.y -= 0.3 + strength * 0.5; // sag

  const curve = new THREE.QuadraticBezierCurve3(from, mid, to);
  const points = curve.getPoints(20);
  const path = new THREE.CatmullRomCurve3(points);

  const thickness = 0.015 + strength * 0.02;
  const geo = new THREE.TubeGeometry(path, 16, thickness, 4, false);

  const mat = new THREE.MeshStandardMaterial({
    color: 0x5A7A4A,
    roughness: 0.9,
    transparent: true,
    opacity: 0.4 + strength * 0.3,
  });

  scene.add(new THREE.Mesh(geo, mat));
}

// ─── Hanging moss ────────────────────────────────────────────────────────────

function buildHangingMoss(scene, rng) {
  // Wispy hanging moss from the larger branch endpoints
  for (const [id, ep] of branchEndpoints) {
    if (ep.radius < 0.1) continue; // only from thicker branches
    if (rng() > 0.6) continue;

    const nStrands = 2 + Math.floor(rng() * 4);
    for (let i = 0; i < nStrands; i++) {
      const start = ep.position.clone().add(
        new THREE.Vector3((rng() - 0.5) * 0.5, -0.1, (rng() - 0.5) * 0.5)
      );
      const length = 0.5 + rng() * 1.5;
      const end = start.clone().add(new THREE.Vector3(
        (rng() - 0.5) * 0.3, -length, (rng() - 0.5) * 0.3,
      ));

      const curve = new THREE.CatmullRomCurve3([
        start,
        start.clone().lerp(end, 0.5).add(new THREE.Vector3((rng() - 0.5) * 0.15, 0, (rng() - 0.5) * 0.15)),
        end,
      ]);
      const geo = new THREE.TubeGeometry(curve, 6, 0.008 + rng() * 0.008, 3, false);
      const mat = new THREE.MeshStandardMaterial({
        color: 0x6A8A5A, roughness: 0.95, transparent: true, opacity: 0.35 + rng() * 0.2,
      });
      scene.add(new THREE.Mesh(geo, mat));
    }
  }
}

// ─── Roots ───────────────────────────────────────────────────────────────────

function buildRoots(scene, rng) {
  const nRoots = 5 + Math.floor(rng() * 4);
  for (let i = 0; i < nRoots; i++) {
    const angle = (i / nRoots) * Math.PI * 2 + rng() * 0.4;
    const length = 1.0 + rng() * 1.5;
    const rootR = 0.06 + rng() * 0.08;

    const start = new THREE.Vector3(
      Math.cos(angle) * TRUNK_RADIUS * 0.7,
      0.2,
      Math.sin(angle) * TRUNK_RADIUS * 0.7,
    );

    const end = new THREE.Vector3(
      Math.cos(angle) * (TRUNK_RADIUS + length),
      -0.15 - rng() * 0.2,
      Math.sin(angle) * (TRUNK_RADIUS + length),
    );

    const mid = start.clone().lerp(end, 0.5);
    mid.y = -0.05 + rng() * 0.1;

    const curve = new THREE.CatmullRomCurve3([start, mid, end]);
    const geo = new THREE.TubeGeometry(curve, 8, rootR, 5, false);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x4A3A28, roughness: 0.95, flatShading: true,
    });
    scene.add(new THREE.Mesh(geo, mat));
  }
}

// ─── Ground ──────────────────────────────────────────────────────────────────

function buildGround(scene) {
  // Forest floor: dead leaves, moss, damp earth
  const geo = new THREE.CircleGeometry(20, 32);
  geo.rotateX(-Math.PI / 2);

  const colors = new Float32Array(geo.attributes.position.count * 3);
  const rng = seededRNG(2718);
  for (let i = 0; i < geo.attributes.position.count; i++) {
    const x = geo.attributes.position.getX(i);
    const z = geo.attributes.position.getZ(i);
    const d = Math.sqrt(x * x + z * z);

    // Near trunk: damp earth. Further out: leaf litter
    const t = Math.min(d / 10, 1);
    let r = 0.12 + t * 0.10 + (rng() - 0.5) * 0.04;
    let g = 0.10 + t * 0.06 + (rng() - 0.5) * 0.03;
    let b = 0.06 + t * 0.03 + (rng() - 0.5) * 0.02;

    // Moss patches near trunk
    if (d < 3 && rng() > 0.5) {
      g += 0.06;
    }

    colors[i * 3] = r;
    colors[i * 3 + 1] = g;
    colors[i * 3 + 2] = b;
  }

  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.95,
    metalness: 0,
  });

  const ground = new THREE.Mesh(geo, mat);
  ground.position.y = -0.05;
  scene.add(ground);

  // A few fallen leaves / small rocks
  const rockGeo = new THREE.DodecahedronGeometry(0.08, 0);
  const rockMat = new THREE.MeshStandardMaterial({ color: 0x605848, roughness: 0.95, flatShading: true });
  const rng2 = seededRNG(1618);
  for (let i = 0; i < 15; i++) {
    const angle = rng2() * Math.PI * 2;
    const dist = 1 + rng2() * 5;
    const rock = new THREE.Mesh(rockGeo, rockMat);
    rock.position.set(Math.cos(angle) * dist, 0, Math.sin(angle) * dist);
    rock.rotation.set(rng2() * Math.PI, rng2() * Math.PI, 0);
    rock.scale.setScalar(0.5 + rng2() * 1.0);
    scene.add(rock);
  }
}

// ─── Sky dome ────────────────────────────────────────────────────────────────

function buildSkyDome(scene) {
  const skyR = 60;
  const skyGeo = new THREE.SphereGeometry(skyR, 16, 12);
  const skyColors = new Float32Array(skyGeo.attributes.position.count * 3);
  const pos = skyGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i) / skyR;
    const t = (y + 1) / 2;
    // Soft overcast — lighter at horizon, slightly blue-grey above
    skyColors[i * 3]     = 0.82 - t * 0.15;
    skyColors[i * 3 + 1] = 0.84 - t * 0.12;
    skyColors[i * 3 + 2] = 0.86 - t * 0.06;
  }
  skyGeo.setAttribute('color', new THREE.BufferAttribute(skyColors, 3));
  const sky = new THREE.Mesh(skyGeo, new THREE.MeshBasicMaterial({
    vertexColors: true, side: THREE.BackSide, fog: false,
  }));
  sky.position.y = 5;
  scene.add(sky);
}
