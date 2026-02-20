// landscape.js — Kheerganga under monsoon.
//
// Real terrain from SRTM DEM. The viewer stands on Kheerganga's meadow
// (~3500m), looking northwest across the Parvati gorge at the mountain
// that rises to nearly 5000m — the most majestic sight in the valley.
//
// Season: monsoon. Valley mist rises from the gorge, clouds cling to
// the mountain's flanks, everything is saturated green below the treeline.
// The gods gather here. The MāyāLucIA conference happens in the meadow.

import * as THREE from 'three';

const KIND = {
  GALAXY_CENTER: 'galaxy-center',
  STAR: 'star',
  PLANET: 'planet',
  MOON: 'moon',
};

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

function hash2(ix, iz) {
  let n = ix * 374761393 + iz * 668265263;
  n = (n ^ (n >> 13)) * 1274126177;
  return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff;
}

// ─── DEM data (loaded async) ─────────────────────────────────────────────────

let demGrid = null;
let demRows = 0, demCols = 0;
let demMinElev = 0, demMaxElev = 0;
let demScale = 1/40;
let demCellSize = 28.5;
let demWorldW = 0, demWorldH = 0;
let kgRow = 240, kgCol = 240;

const CLEARING_RADIUS = 10;   // world units — Kheerganga meadow is large

// ─── DEM sampling ────────────────────────────────────────────────────────────

function sampleH(wx, wz) {
  if (!demGrid) return 0;
  const col = wx / (demCellSize * demScale) + kgCol;
  const row = wz / (demCellSize * demScale) + kgRow;
  const r = Math.max(0, Math.min(demRows - 2, Math.floor(row)));
  const c = Math.max(0, Math.min(demCols - 2, Math.floor(col)));
  const fr = row - r, fc = col - c;
  const h00 = demGrid[r * demCols + c];
  const h10 = demGrid[r * demCols + c + 1];
  const h01 = demGrid[(r + 1) * demCols + c];
  const h11 = demGrid[(r + 1) * demCols + c + 1];
  const elev = h00*(1-fr)*(1-fc) + h10*(1-fr)*fc + h01*fr*(1-fc) + h11*fr*fc;
  return (elev - demMinElev) * demScale;
}

function elevAt(wx, wz) {
  return sampleH(wx, wz) / demScale + demMinElev;
}

// ─── Module state ────────────────────────────────────────────────────────────

let campSites = [];
let clearingCenter = { x: 0, z: 0 };

// ─── Theme export ────────────────────────────────────────────────────────────

export default {
  getSceneDefaults() {
    return {
      background: 0x8A9AA8,           // monsoon overcast
      cameraPos: [5, 38, 20],         // on the meadow, slightly elevated
      cameraTarget: [-60, 40, -60],   // looking NW at the mountain
      cameraNear: 0.5,
      cameraFar: 600,
      orbitMinDistance: 3,
      orbitMaxDistance: 350,
      bloomStrength: 0.15,
      bloomRadius: 0.8,
      bloomThreshold: 0.85,
    };
  },

  renderEnvironment(scene) {
    campSites = [];
    clearingCenter = { x: 0, z: 0 };

    // Monsoon light: soft, diffuse, no harsh shadows
    scene.add(new THREE.HemisphereLight(0x9AAAB8, 0x405838, 0.55));

    // Weak sun filtering through cloud cover — slightly warm
    const sun = new THREE.DirectionalLight(0xE8D8C0, 0.5);
    sun.position.set(20, 40, 30);
    scene.add(sun);

    // Cool fill from the mountain side
    const fill = new THREE.DirectionalLight(0x8898A8, 0.25);
    fill.position.set(-40, 15, -30);
    scene.add(fill);

    scene.add(new THREE.AmbientLight(0x556065, 0.2));

    // Monsoon fog — thick in the gorge, thins at altitude
    scene.fog = new THREE.FogExp2(0x8A9AA8, 0.004);

    buildSkyDome(scene);
    buildMonsoonClouds(scene);
  },

  renderBody(scene, body, position) {
    const kind = body.kind || KIND.MOON;
    const [r, g, b] = body.color || [0.5, 0.5, 0.5];

    const scale = 0.6;
    const cx = clearingCenter.x + position.x * scale;
    const cz = clearingCenter.z + position.z * scale;

    campSites.push({
      x: cx, z: cz, kind,
      color: [r, g, b],
      id: body.id,
      label: body.label,
      mass: body.mass || 0.5,
      clearingR: kind === KIND.GALAXY_CENTER ? 3.5 :
                 kind === KIND.STAR ? 1.8 :
                 kind === KIND.PLANET ? 1.0 : 0.5,
    });

    if (kind === KIND.GALAXY_CENTER) {
      clearingCenter.x = cx;
      clearingCenter.z = cz;
    }

    const markerR =
      kind === KIND.GALAXY_CENTER ? 3.5 :
      kind === KIND.STAR ? 1.8 :
      kind === KIND.PLANET ? 1.0 : 0.5;
    const markerGeo = new THREE.SphereGeometry(markerR, 8, 6);
    const markerMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false });
    const marker = new THREE.Mesh(markerGeo, markerMat);
    marker.position.set(cx, 5, cz);
    marker.userData = { bodyId: body.id, body, baseEmissive: 0, peakX: cx, peakZ: cz };
    scene.add(marker);
    return marker;
  },

  renderBond(scene, bond, fromPos, toPos) {
    if (!this._bonds) this._bonds = [];
    const s = 0.6;
    this._bonds.push({
      fromPos: { x: clearingCenter.x + fromPos.x * s, z: clearingCenter.z + fromPos.z * s },
      toPos: { x: clearingCenter.x + toPos.x * s, z: clearingCenter.z + toPos.z * s },
      strength: bond.strength || 0.5,
    });
    const geo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ visible: false }));
    scene.add(line);
    return line;
  },

  highlightBody(mesh, active) {
    if (!mesh || !mesh.userData.body) return;
    const fire = mesh.userData._fireLight;
    if (fire) fire.intensity = active ? 4.0 : fire.userData?.baseIntensity || 1.0;
    const beacon = mesh.userData._beacon;
    if (beacon) {
      beacon.material.emissiveIntensity = active ? 1.5 : 0.3;
      beacon.scale.setScalar(active ? 1.5 : 1.0);
    }
  },

  async generateTerrain(scene, camera, controls) {
    const resp = await fetch('./kheerganga_dem.json');
    const dem = await resp.json();

    demRows = dem.rows;
    demCols = dem.cols;
    demMinElev = dem.min_elev;
    demMaxElev = dem.max_elev;
    demScale = dem.scale;
    demCellSize = dem.cell_size_m;
    kgRow = dem.kheerganga.row;
    kgCol = dem.kheerganga.col;
    demGrid = new Float32Array(dem.elevation);
    demWorldW = demCols * demCellSize * demScale;
    demWorldH = demRows * demCellSize * demScale;

    // 1. Build terrain mesh from real DEM
    buildTerrain(scene);

    // 2. Position camera at Kheerganga looking at the mountain
    const kgH = sampleH(0, 0);
    if (camera && controls) {
      // Stand on the meadow, look NW across the gorge
      camera.position.set(5, kgH + 6, 8);
      controls.target.set(-40, kgH + 15, -40);
      camera.lookAt(-40, kgH + 15, -40);
      controls.update();
    }

    // 3. Correct marker heights
    scene.traverse(obj => {
      if (obj.userData?.peakX !== undefined) {
        obj.position.y = sampleH(obj.userData.peakX, obj.userData.peakZ) + 1.5;
      }
    });

    // 4. Dense monsoon forest
    buildForests(scene);

    // 5. Hot springs
    buildHotSprings(scene);

    // 6. Shiva temple
    buildShivaTemple(scene);

    // 7. Camps — the gathering
    for (const camp of campSites) {
      buildCamp(scene, camp, sampleH(camp.x, camp.z));
    }

    // 8. Trails between camps
    for (const b of (this._bonds || [])) {
      buildTrail(scene, b.fromPos, b.toPos, b.strength);
    }

    // 9. Clearing glow — warm light in the mist
    buildClearingGlow(scene);

    // 10. Parvati river in the gorge
    buildWater(scene);

    // 11. Rocks above treeline
    buildRockScatter(scene);

    // 12. Valley mist — monsoon fog rising from gorge
    buildValleyMist(scene);
  },
};

// ─── Terrain mesh ────────────────────────────────────────────────────────────

function buildTerrain(scene) {
  const geo = new THREE.PlaneGeometry(demWorldW, demWorldH, demCols - 1, demRows - 1);
  geo.rotateX(-Math.PI / 2);

  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);

  for (let i = 0; i < pos.count; i++) {
    const gridCol = i % demCols;
    const gridRow = Math.floor(i / demCols);

    const wx = (gridCol - kgCol) * demCellSize * demScale;
    const wz = (gridRow - kgRow) * demCellSize * demScale;
    const elev = demGrid[gridRow * demCols + gridCol];
    const h = (elev - demMinElev) * demScale;

    pos.setX(i, wx);
    pos.setZ(i, wz);
    pos.setY(i, h);
  }

  geo.computeVertexNormals();

  const normals = geo.attributes.normal;
  for (let i = 0; i < pos.count; i++) {
    const elev = pos.getY(i) / demScale + demMinElev;
    const ny = normals.getY(i);
    const wx = pos.getX(i), wz = pos.getZ(i);
    colorVertex(colors, i, elev, ny, wx, wz);
  }

  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.92,
    metalness: 0.0,
    flatShading: false,
  });

  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);
  return mesh;
}

function colorVertex(colors, i, elev, normalY, wx, wz) {
  const steepness = 1.0 - normalY;

  // Clearing blend
  const dx = wx - clearingCenter.x, dz = wz - clearingCenter.z;
  const distFromClearing = Math.sqrt(dx * dx + dz * dz);
  const inClearing = distFromClearing < CLEARING_RADIUS;

  let r, g, b;

  // Monsoon Parvati Valley altitude bands (elevation in meters):
  // The colours are saturated, wet, alive.
  if (elev > 4800) {
    // Snow patches and ice — even in monsoon, these heights hold snow
    const t = Math.min((elev - 4800) / 600, 1);
    r = 0.85 + t * 0.10; g = 0.88 + t * 0.08; b = 0.92 + t * 0.06;
    // Steep rock faces show through
    if (steepness > 0.30) {
      const s = (steepness - 0.30) / 0.70;
      r = r * (1-s) + 0.38 * s; g = g * (1-s) + 0.34 * s; b = b * (1-s) + 0.32 * s;
    }
  } else if (elev > 4200) {
    // Alpine rock and scree — grey-brown, wet, some lichen
    const t = (elev - 4200) / 600;
    r = 0.32 + t * 0.18; g = 0.30 + t * 0.12; b = 0.28 + t * 0.14;
    if (steepness < 0.12) { g += 0.06; } // wet lichen on flat rocks
  } else if (elev > 3800) {
    // Subalpine meadow and krummholz — bright monsoon green fading to rock
    const t = (elev - 3800) / 400;
    r = 0.12 + t * 0.15; g = 0.28 - t * 0.02; b = 0.08 + t * 0.12;
    if (steepness > 0.40) { r = 0.34; g = 0.30; b = 0.26; }
  } else if (elev > 3400) {
    // Dense conifer forest — dark monsoon green, very saturated
    const t = (elev - 3400) / 400;
    r = 0.04 + t * 0.06; g = 0.14 + t * 0.10; b = 0.03 + t * 0.04;
    if (steepness > 0.40) {
      const s = (steepness - 0.40) / 0.60;
      r = r * (1-s) + 0.28 * s; g = g * (1-s) + 0.22 * s; b = b * (1-s) + 0.18 * s;
    }
  } else if (elev > 3000) {
    // Mixed forest: deodar, blue pine, oak — lush monsoon canopy
    const t = (elev - 3000) / 400;
    r = 0.03 + t * 0.03; g = 0.12 + t * 0.06; b = 0.02 + t * 0.02;
  } else if (elev > 2600) {
    // Valley slopes — dense subtropical, deep green
    const t = (elev - 2600) / 400;
    r = 0.05 + t * 0.02; g = 0.15 + t * 0.03; b = 0.04 + t * 0.01;
  } else {
    // River gorge floor
    r = 0.08; g = 0.12; b = 0.08;
  }

  // Kheerganga meadow — green grass, wildflowers in monsoon
  if (inClearing) {
    const clearT = 1 - distFromClearing / CLEARING_RADIUS;
    const blend = clearT * 0.7;
    // Monsoon meadow: vivid green with tiny yellow wildflower hints
    r = r * (1 - blend) + 0.18 * blend;
    g = g * (1 - blend) + 0.40 * blend;
    b = b * (1 - blend) + 0.10 * blend;
  }

  // Subtle noise
  const noise = (hash2(Math.floor(i * 7.3), Math.floor(i * 13.7)) - 0.5) * 0.018;
  colors[i * 3]     = Math.max(0, Math.min(1, r + noise));
  colors[i * 3 + 1] = Math.max(0, Math.min(1, g + noise));
  colors[i * 3 + 2] = Math.max(0, Math.min(1, b + noise));
}

// ─── Hot springs ─────────────────────────────────────────────────────────────

function buildHotSprings(scene) {
  const h = sampleH(0, 0);
  const stoneMat = new THREE.MeshStandardMaterial({ color: 0x606055, roughness: 0.95, flatShading: true });
  const rng = seededRNG(42);

  // Kund (pool) — ring of weathered boulders
  const poolR = 1.5;
  for (let i = 0; i < 14; i++) {
    const angle = (i / 14) * Math.PI * 2;
    const sr = 0.12 + rng() * 0.14;
    const stone = new THREE.Mesh(new THREE.DodecahedronGeometry(sr, 0), stoneMat);
    stone.position.set(
      Math.cos(angle) * (poolR + (rng() - 0.5) * 0.3),
      h + sr * 0.25,
      Math.sin(angle) * (poolR + (rng() - 0.5) * 0.3),
    );
    stone.rotation.set(rng() * Math.PI, rng() * Math.PI, 0);
    scene.add(stone);
  }

  // Warm turquoise water
  const pool = new THREE.Mesh(
    new THREE.CircleGeometry(poolR * 0.8, 16),
    new THREE.MeshStandardMaterial({
      color: 0x5AACA0, emissive: 0x2A6A60, emissiveIntensity: 0.12,
      transparent: true, opacity: 0.55, roughness: 0.1, side: THREE.DoubleSide,
    })
  );
  pool.rotation.x = -Math.PI / 2;
  pool.position.set(0, h + 0.04, 0);
  scene.add(pool);

  // Steam — more prominent in monsoon cool air
  const steamMat = new THREE.MeshStandardMaterial({
    color: 0xDDDDDD, transparent: true, roughness: 1,
    depthWrite: false, side: THREE.DoubleSide,
  });
  for (let i = 0; i < 12; i++) {
    const wispH = 3 + rng() * 5;
    const wispR = 0.25 + rng() * 0.4;
    const wisp = new THREE.Mesh(
      new THREE.ConeGeometry(wispR, wispH, 6, 1, true),
      steamMat.clone()
    );
    wisp.material.opacity = 0.025 + rng() * 0.04;
    wisp.position.set(
      (rng() - 0.5) * poolR * 0.7,
      h + 0.5 + i * wispH * 0.25,
      (rng() - 0.5) * poolR * 0.7,
    );
    scene.add(wisp);
  }

  scene.add(new THREE.PointLight(0x88CCAA, 0.6, 10));
}

// ─── Shiva temple ────────────────────────────────────────────────────────────

function buildShivaTemple(scene) {
  const tx = 3, tz = -2;
  const h = sampleH(tx, tz);
  const stoneMat = new THREE.MeshStandardMaterial({ color: 0x807870, roughness: 0.92, flatShading: true });

  // Platform
  const plat = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.25, 1.8), stoneMat);
  plat.position.set(tx, h + 0.12, tz);
  scene.add(plat);

  // Body
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.3, 1.1), stoneMat);
  body.position.set(tx, h + 0.85, tz);
  scene.add(body);

  // Shikhara
  const shik = new THREE.Mesh(
    new THREE.ConeGeometry(0.55, 1.1, 6),
    new THREE.MeshStandardMaterial({ color: 0x908880, roughness: 0.88, flatShading: true })
  );
  shik.position.set(tx, h + 2.0, tz);
  scene.add(shik);

  // Saffron flag
  const pole = new THREE.Mesh(
    new THREE.CylinderGeometry(0.015, 0.02, 1.8, 4),
    new THREE.MeshStandardMaterial({ color: 0x8B7355, roughness: 0.9 })
  );
  pole.position.set(tx + 0.7, h + 2.4, tz);
  scene.add(pole);

  const flag = new THREE.Mesh(
    new THREE.PlaneGeometry(0.55, 0.35),
    new THREE.MeshStandardMaterial({
      color: 0xFF6600, emissive: 0xFF4400, emissiveIntensity: 0.08,
      side: THREE.DoubleSide, roughness: 0.7,
    })
  );
  flag.position.set(tx + 0.98, h + 3.0, tz);
  scene.add(flag);

  // Bell
  const bell = new THREE.Mesh(
    new THREE.SphereGeometry(0.07, 6, 4, 0, Math.PI * 2, 0, Math.PI * 0.6),
    new THREE.MeshStandardMaterial({ color: 0xB87333, roughness: 0.3, metalness: 0.7 })
  );
  bell.position.set(tx, h + 1.55, tz - 0.6);
  scene.add(bell);
}

// ─── Clearing glow ───────────────────────────────────────────────────────────

function buildClearingGlow(scene) {
  const h = sampleH(clearingCenter.x, clearingCenter.z);

  // Warm fire glow — visible through monsoon mist
  const mainGlow = new THREE.PointLight(0xFF8833, 4.0, 60);
  mainGlow.position.set(clearingCenter.x, h + 3, clearingCenter.z);
  scene.add(mainGlow);

  // Light catching the mist above
  const mistGlow = new THREE.PointLight(0xFFAA55, 1.2, 40);
  mistGlow.position.set(clearingCenter.x, h + 10, clearingCenter.z);
  scene.add(mistGlow);
}

// ─── Forests — monsoon dense ─────────────────────────────────────────────────

function buildForests(scene) {
  const rng = seededRNG(31415);

  const trunkGeo = new THREE.CylinderGeometry(0.04, 0.09, 1.0, 5);
  const coniferGeo = new THREE.ConeGeometry(0.35, 1.4, 6);
  const broadGeo = new THREE.SphereGeometry(0.45, 6, 4);

  const maxTrees = 8000;
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x2A1A0A, roughness: 0.92 });
  // Monsoon greens: darker, wetter, more saturated
  const coniferMat = new THREE.MeshStandardMaterial({ color: 0x0A2A0A, roughness: 0.88, flatShading: true });
  const broadMat = new THREE.MeshStandardMaterial({ color: 0x0E3A0E, roughness: 0.82, flatShading: true });

  const trunkInst = new THREE.InstancedMesh(trunkGeo, trunkMat, maxTrees);
  const coniferInst = new THREE.InstancedMesh(coniferGeo, coniferMat, maxTrees);
  const broadInst = new THREE.InstancedMesh(broadGeo, broadMat, maxTrees);

  const dummy = new THREE.Object3D();
  const col = new THREE.Color();
  let tCount = 0, cCount = 0, bCount = 0;

  const halfW = demWorldW / 2, halfH = demWorldH / 2;
  const step = demWorldW / 160;  // denser for monsoon

  for (let gx = -halfW; gx < halfW && tCount < maxTrees; gx += step) {
    for (let gz = -halfH; gz < halfH && tCount < maxTrees; gz += step) {
      const x = gx + (rng() - 0.5) * step * 1.4;
      const z = gz + (rng() - 0.5) * step * 1.4;
      const h = sampleH(x, z);
      const elev = h / demScale + demMinElev;

      // Treeline: 2600m (valley) to 3900m (subalpine)
      if (elev < 2600 || elev > 3900) continue;

      // Density by altitude band
      const belt =
        elev < 2700 ? (elev - 2600) / 100 :
        elev > 3700 ? (3900 - elev) / 200 : 1.0;
      if (rng() > belt * 0.88) continue;

      // Clear the conference meadow
      const dx = x - clearingCenter.x, dz = z - clearingCenter.z;
      const dClearing = Math.sqrt(dx * dx + dz * dz);
      if (dClearing < CLEARING_RADIUS) {
        if (dClearing < CLEARING_RADIUS * 0.75) continue;
        if (rng() > 0.1) continue;
      }

      // Skip near camps
      let nearCamp = false;
      for (const c of campSites) {
        if ((x - c.x) ** 2 + (z - c.z) ** 2 < c.clearingR ** 2 * 1.5) {
          nearCamp = true; break;
        }
      }
      if (nearCamp) continue;

      const treeH = 1.0 + rng() * 2.0;
      const treeScale = 0.5 + rng() * 0.8;

      const isConifer = elev > 3200 || rng() > 0.30;
      const isBirch = elev > 3500 && rng() > 0.45;

      dummy.position.set(x, h + treeH * 0.35, z);
      dummy.scale.set(treeScale * 0.6, treeH, treeScale * 0.6);
      dummy.rotation.set(0, rng() * Math.PI * 2, 0);
      dummy.updateMatrix();
      trunkInst.setMatrixAt(tCount, dummy.matrix);
      tCount++;

      if (isBirch || !isConifer) {
        dummy.position.set(x, h + treeH * 1.05, z);
        dummy.scale.set(treeScale * 1.1, treeH * 0.75, treeScale * 1.1);
        dummy.updateMatrix();
        broadInst.setMatrixAt(bCount, dummy.matrix);
        const green = isBirch ? 0.18 + rng() * 0.10 : 0.12 + rng() * 0.10;
        col.setRGB(0.03 + rng() * 0.04, green, 0.02 + rng() * 0.03);
        broadInst.setColorAt(bCount, col);
        bCount++;
      } else {
        dummy.position.set(x, h + treeH * 1.0, z);
        dummy.scale.set(treeScale * 0.85, treeH * 1.35, treeScale * 0.85);
        dummy.updateMatrix();
        coniferInst.setMatrixAt(cCount, dummy.matrix);
        const green = 0.06 + rng() * 0.08;
        col.setRGB(0.01 + rng() * 0.02, green, 0.01 + rng() * 0.02);
        coniferInst.setColorAt(cCount, col);
        cCount++;
      }
    }
  }

  trunkInst.count = tCount;
  coniferInst.count = cCount;
  broadInst.count = bCount;
  trunkInst.instanceMatrix.needsUpdate = true;
  coniferInst.instanceMatrix.needsUpdate = true;
  broadInst.instanceMatrix.needsUpdate = true;
  if (coniferInst.instanceColor) coniferInst.instanceColor.needsUpdate = true;
  if (broadInst.instanceColor) broadInst.instanceColor.needsUpdate = true;

  scene.add(trunkInst);
  scene.add(coniferInst);
  scene.add(broadInst);
}

// ─── Camps ───────────────────────────────────────────────────────────────────

function buildCamp(scene, camp, h) {
  const color = new THREE.Color(camp.color[0], camp.color[1], camp.color[2]);
  const rng = seededRNG(hashStr(camp.id));
  if (camp.kind === KIND.GALAXY_CENTER) buildMainGathering(scene, camp, h, color, rng);
  else if (camp.kind === KIND.STAR) buildBaseCamp(scene, camp, h, color, rng);
  else if (camp.kind === KIND.PLANET) buildSmallCamp(scene, camp, h, color, rng);
  else buildSoloCamp(scene, camp, h, color, rng);
}

function buildMainGathering(scene, camp, h, color, rng) {
  const x = camp.x, z = camp.z;

  // Shamiana — rain shelter for monsoon
  const poleH = 3.0;
  const canopyR = 2.5;
  const poleMat = new THREE.MeshStandardMaterial({ color: 0x5B3216, roughness: 0.9 });
  const poleGeo = new THREE.CylinderGeometry(0.04, 0.06, poleH, 5);
  for (const [px, pz] of [[-canopyR, canopyR], [canopyR, canopyR], [canopyR, -canopyR], [-canopyR, -canopyR]]) {
    const pole = new THREE.Mesh(poleGeo, poleMat);
    pole.position.set(x + px, sampleH(x + px, z + pz) + poleH / 2, z + pz);
    scene.add(pole);
  }

  // Canvas canopy — slightly sagging, warm toned
  const canopyGeo = new THREE.PlaneGeometry(canopyR * 2, canopyR * 2, 10, 10);
  canopyGeo.rotateX(-Math.PI / 2);
  const cpos = canopyGeo.attributes.position;
  for (let i = 0; i < cpos.count; i++) {
    const cx = cpos.getX(i), cz = cpos.getZ(i);
    const d = Math.sqrt(cx * cx + cz * cz) / canopyR;
    cpos.setY(i, cpos.getY(i) - d * d * 0.5 + 0.2);
  }
  canopyGeo.computeVertexNormals();
  const canopy = new THREE.Mesh(canopyGeo, new THREE.MeshStandardMaterial({
    color: 0xC8B898, side: THREE.DoubleSide, transparent: true, opacity: 0.55,
    roughness: 0.85, emissive: color, emissiveIntensity: 0.03,
  }));
  canopy.position.set(x, h + poleH - 0.35, z);
  scene.add(canopy);

  buildFirePit(scene, x, h, z, 0.5, color, camp);
  buildPrayerFlags(scene, x, h, z, x + 4, sampleH(x + 4, z - 2.5), z - 2.5);
  buildPrayerFlags(scene, x, h, z, x - 3.5, sampleH(x - 3.5, z + 2), z + 2);
  buildSmoke(scene, x, h + 0.3, z, 1.0);
}

function buildBaseCamp(scene, camp, h, color, rng) {
  const x = camp.x, z = camp.z;
  const nTents = 2 + Math.floor(rng() * 2);
  for (let i = 0; i < nTents; i++) {
    const angle = (i / nTents) * Math.PI * 2 + rng() * 0.5;
    const tx = x + Math.cos(angle) * 1.2;
    const tz = z + Math.sin(angle) * 1.2;
    buildTent(scene, tx, sampleH(tx, tz), tz, 0.45, color, angle + Math.PI, rng);
  }
  buildFirePit(scene, x, h, z, 0.28, color, camp);
  buildSmoke(scene, x, h + 0.15, z, 0.5);
}

function buildSmallCamp(scene, camp, h, color, rng) {
  const x = camp.x, z = camp.z;
  buildTent(scene, x, h, z, 0.35, color, rng() * Math.PI * 2, rng);
  buildFirePit(scene, x + 0.45, sampleH(x + 0.45, z + 0.3), z + 0.3, 0.18, color, camp);
  buildSmoke(scene, x + 0.45, sampleH(x + 0.45, z + 0.3) + 0.1, z + 0.3, 0.3);
}

function buildSoloCamp(scene, camp, h, color, rng) {
  const x = camp.x, z = camp.z;
  if (rng() > 0.25) buildTent(scene, x, h, z, 0.22, color, rng() * Math.PI * 2, rng);
  const beacon = new THREE.Mesh(
    new THREE.SphereGeometry(0.06, 8, 6),
    new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.3, transparent: true, opacity: 0.5 })
  );
  beacon.position.set(x, h + 0.4, z);
  scene.add(beacon);
  scene.traverse(obj => {
    if (obj.userData?.peakX === camp.x && obj.userData?.peakZ === camp.z) obj.userData._beacon = beacon;
  });
}

// ─── Tent ────────────────────────────────────────────────────────────────────

function buildTent(scene, x, h, z, size, color, facing, rng) {
  const halfW = size * 0.5, halfD = size * 0.7, ridgeH = size * 0.6;
  const verts = new Float32Array([
    -halfW,0,-halfD, 0,ridgeH,-halfD, -halfW,0,halfD,
    0,ridgeH,-halfD, 0,ridgeH,halfD, -halfW,0,halfD,
    halfW,0,-halfD, halfW,0,halfD, 0,ridgeH,-halfD,
    0,ridgeH,-halfD, halfW,0,halfD, 0,ridgeH,halfD,
    -halfW,0,-halfD, halfW,0,-halfD, 0,ridgeH,-halfD,
    -halfW,0,halfD, 0,ridgeH,halfD, halfW,0,halfD,
  ]);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
  geo.computeVertexNormals();
  const fabricColor = color.clone().lerp(new THREE.Color(0.80, 0.75, 0.65), 0.35);
  const mat = new THREE.MeshStandardMaterial({
    color: fabricColor, roughness: 0.88, side: THREE.DoubleSide,
    emissive: color, emissiveIntensity: 0.05,
  });
  const tent = new THREE.Mesh(geo, mat);
  tent.position.set(x, h, z);
  tent.rotation.y = facing;
  scene.add(tent);
}

// ─── Fire pit ────────────────────────────────────────────────────────────────

function buildFirePit(scene, x, h, z, radius, color, camp) {
  const stoneMat = new THREE.MeshStandardMaterial({ color: 0x504540, roughness: 0.95, flatShading: true });
  const nStones = 6 + Math.floor(radius * 5);
  for (let i = 0; i < nStones; i++) {
    const angle = (i / nStones) * Math.PI * 2;
    const stone = new THREE.Mesh(
      new THREE.DodecahedronGeometry(0.05 + radius * 0.04, 0),
      stoneMat
    );
    stone.position.set(x + Math.cos(angle) * radius, h + 0.03, z + Math.sin(angle) * radius);
    stone.rotation.set(Math.random(), Math.random(), 0);
    scene.add(stone);
  }
  const embers = new THREE.Mesh(
    new THREE.CircleGeometry(radius * 0.6, 8),
    new THREE.MeshStandardMaterial({ color: 0xFF4400, emissive: 0xFF6600, emissiveIntensity: 0.9, roughness: 0.5, side: THREE.DoubleSide })
  );
  embers.rotation.x = -Math.PI / 2;
  embers.position.set(x, h + 0.03, z);
  scene.add(embers);

  const intensity = camp.kind === KIND.GALAXY_CENTER ? 2.5 : camp.kind === KIND.STAR ? 1.0 : 0.5;
  const range = camp.kind === KIND.GALAXY_CENTER ? 14 : camp.kind === KIND.STAR ? 7 : 3.5;
  const fireLight = new THREE.PointLight(0xFF8844, intensity, range);
  fireLight.position.set(x, h + 0.4, z);
  fireLight.userData = { baseIntensity: intensity };
  scene.add(fireLight);

  scene.traverse(obj => {
    if (obj.userData?.peakX === camp.x && obj.userData?.peakZ === camp.z) {
      obj.userData._fireLight = fireLight;
      obj.userData._beacon = embers;
    }
  });
}

// ─── Smoke ───────────────────────────────────────────────────────────────────

function buildSmoke(scene, x, h, z, scale) {
  const mat = new THREE.MeshStandardMaterial({
    color: 0xBBBBBB, transparent: true, roughness: 1, depthWrite: false, side: THREE.DoubleSide,
  });
  const rng = seededRNG(hashStr(`smoke${x}${z}`));
  for (let i = 0; i < 4 + Math.floor(scale * 4); i++) {
    const wH = 2 + rng() * 3 * scale;
    const wR = 0.2 + rng() * 0.3 * scale;
    const wisp = new THREE.Mesh(new THREE.ConeGeometry(wR, wH, 6, 1, true), mat.clone());
    wisp.material.opacity = 0.025 + rng() * 0.04;
    wisp.position.set(x + (rng() - 0.5) * 0.3, h + 0.3 + i * wH * 0.28, z + (rng() - 0.5) * 0.3);
    scene.add(wisp);
  }
}

// ─── Prayer flags ────────────────────────────────────────────────────────────

function buildPrayerFlags(scene, x1, h1, z1, x2, h2, z2) {
  const poleMat = new THREE.MeshStandardMaterial({ color: 0x8B7355, roughness: 0.9 });
  const poleGeo = new THREE.CylinderGeometry(0.02, 0.03, 2.0, 4);
  for (const [px, py, pz] of [[x1, h1, z1], [x2, h2, z2]]) {
    const pole = new THREE.Mesh(poleGeo, poleMat);
    pole.position.set(px, py + 1.0, pz);
    scene.add(pole);
  }
  const flagColors = [0x2244BB, 0xEEEEEE, 0xCC2222, 0x22AA44, 0xEECC22];
  for (let i = 0; i < 8; i++) {
    const t = (i + 0.5) / 8;
    const fx = x1 + (x2 - x1) * t, fz = z1 + (z2 - z1) * t;
    const fy = (h1 + 2.0) + ((h2 + 2.0) - (h1 + 2.0)) * t - Math.sin(t * Math.PI) * 0.4;
    const flag = new THREE.Mesh(
      new THREE.PlaneGeometry(0.16, 0.22),
      new THREE.MeshStandardMaterial({
        color: flagColors[i % 5], side: THREE.DoubleSide, roughness: 0.75,
        emissive: new THREE.Color(flagColors[i % 5]), emissiveIntensity: 0.025,
      })
    );
    flag.position.set(fx, fy, fz);
    flag.lookAt(x2, fy, z2);
    scene.add(flag);
  }
}

// ─── Trails ──────────────────────────────────────────────────────────────────

function buildTrail(scene, fromPos, toPos, strength) {
  const dx = toPos.x - fromPos.x, dz = toPos.z - fromPos.z;
  const len = Math.sqrt(dx * dx + dz * dz);
  if (len < 0.01) return;
  const nSamples = Math.max(12, Math.floor(len * 3));
  const perpX = -dz / len, perpZ = dx / len;
  const points = [];
  for (let i = 0; i <= nSamples; i++) {
    const t = i / nSamples;
    const x = fromPos.x + dx * t + perpX * Math.sin(t * Math.PI * 2) * len * 0.02;
    const z = fromPos.z + dz * t + perpZ * Math.sin(t * Math.PI * 2) * len * 0.02;
    points.push(new THREE.Vector3(x, sampleH(x, z) + 0.03, z));
  }
  const curve = new THREE.CatmullRomCurve3(points);
  const geo = new THREE.TubeGeometry(curve, nSamples, 0.05 + strength * 0.04, 4, false);
  scene.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0x7B6D5B, roughness: 0.95 })));
}

// ─── Rock scatter ────────────────────────────────────────────────────────────

function buildRockScatter(scene) {
  const rng = seededRNG(27182);
  const geo = new THREE.DodecahedronGeometry(1, 0);
  const mat = new THREE.MeshStandardMaterial({ color: 0x555048, roughness: 0.95, flatShading: true });
  const inst = new THREE.InstancedMesh(geo, mat, 500);
  const dummy = new THREE.Object3D();
  let count = 0;

  for (let i = 0; i < 1500 && count < 500; i++) {
    const x = (rng() - 0.5) * demWorldW * 0.8;
    const z = (rng() - 0.5) * demWorldH * 0.8;
    const h = sampleH(x, z);
    const elev = h / demScale + demMinElev;
    if (elev < 3800 || elev > 5000) continue;
    if (rng() > 0.5) continue;
    const s = 0.08 + rng() * 0.35;
    dummy.position.set(x, h + s * 0.25, z);
    dummy.scale.set(s * (0.6 + rng() * 0.5), s * (0.4 + rng() * 0.5), s * (0.6 + rng() * 0.5));
    dummy.rotation.set(rng() * Math.PI, rng() * Math.PI, rng() * 0.5);
    dummy.updateMatrix();
    inst.setMatrixAt(count, dummy.matrix);
    count++;
  }
  inst.count = count;
  inst.instanceMatrix.needsUpdate = true;
  scene.add(inst);
}

// ─── Water (Parvati river) ───────────────────────────────────────────────────

function buildWater(scene) {
  const waterGeo = new THREE.PlaneGeometry(demWorldW, demWorldH);
  waterGeo.rotateX(-Math.PI / 2);
  const waterMat = new THREE.MeshStandardMaterial({
    color: 0x2A5A6F, transparent: true, opacity: 0.5,
    roughness: 0.08, metalness: 0.15,
    emissive: 0x0A2838, emissiveIntensity: 0.06,
  });
  const water = new THREE.Mesh(waterGeo, waterMat);
  // Gorge floor — the Parvati runs about 2500-2600m here
  water.position.y = (2550 - demMinElev) * demScale;
  scene.add(water);
}

// ─── Valley mist — monsoon fog filling the gorge ─────────────────────────────

function buildValleyMist(scene) {
  const rng = seededRNG(7919);

  // Layered fog planes at different heights in the gorge
  const mistMat = new THREE.MeshStandardMaterial({
    color: 0x9AAAB4, transparent: true, roughness: 1,
    depthWrite: false, side: THREE.DoubleSide,
  });

  // Ground-hugging mist layers in the gorge (west of KG)
  for (let i = 0; i < 20; i++) {
    const x = (rng() - 0.8) * demWorldW * 0.5;  // biased west toward gorge
    const z = (rng() - 0.5) * demWorldH * 0.6;
    const h = sampleH(x, z);
    const elev = h / demScale + demMinElev;

    // Only in the gorge and lower slopes
    if (elev > 3200) continue;

    const mistH = 1 + rng() * 3;
    const mistW = 8 + rng() * 15;
    const mist = new THREE.Mesh(
      new THREE.PlaneGeometry(mistW, mistH),
      mistMat.clone()
    );
    mist.material.opacity = 0.04 + rng() * 0.06;
    mist.position.set(x, h + mistH * 0.4, z);
    mist.rotation.y = rng() * Math.PI;
    scene.add(mist);
  }

  // Thicker mist belt partway up the mountain — monsoon clouds clinging
  for (let i = 0; i < 30; i++) {
    const x = (rng() - 0.7) * demWorldW * 0.5;
    const z = (rng() - 0.5) * demWorldH * 0.6;
    const h = sampleH(x, z);
    const elev = h / demScale + demMinElev;

    // Cloud belt: 3500-4200m on the mountain
    if (elev < 3500 || elev > 4200) continue;

    const cloudW = 5 + rng() * 12;
    const cloudH = 2 + rng() * 4;
    const cloud = new THREE.Mesh(
      new THREE.PlaneGeometry(cloudW, cloudH),
      mistMat.clone()
    );
    cloud.material.opacity = 0.03 + rng() * 0.05;
    cloud.position.set(x, h + cloudH * 0.3, z);
    cloud.rotation.y = rng() * Math.PI;
    cloud.rotation.x = (rng() - 0.5) * 0.2;
    scene.add(cloud);
  }
}

// ─── Sky dome — monsoon overcast ─────────────────────────────────────────────

function buildSkyDome(scene) {
  const skyR = demWorldW * 0.9;
  const skyGeo = new THREE.SphereGeometry(skyR, 16, 12);
  const skyColors = new Float32Array(skyGeo.attributes.position.count * 3);
  const pos = skyGeo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i) / skyR;
    const t = (y + 1) / 2;
    // Monsoon sky: grey-white overcast, slightly warm at horizon
    skyColors[i * 3]     = 0.72 - t * 0.20;
    skyColors[i * 3 + 1] = 0.70 - t * 0.18;
    skyColors[i * 3 + 2] = 0.68 - t * 0.10;
  }
  skyGeo.setAttribute('color', new THREE.BufferAttribute(skyColors, 3));
  const sky = new THREE.Mesh(skyGeo, new THREE.MeshBasicMaterial({
    vertexColors: true, side: THREE.BackSide, fog: false,
  }));
  sky.position.y = 20;
  scene.add(sky);
}

// ─── Monsoon clouds ──────────────────────────────────────────────────────────

function buildMonsoonClouds(scene) {
  const geo = new THREE.SphereGeometry(1, 8, 6);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xCCC8C0, transparent: true, roughness: 1, depthWrite: false,
  });
  const rng = seededRNG(9973);
  const group = new THREE.Group();

  // Heavy, low clouds — monsoon character
  for (let i = 0; i < 35; i++) {
    const cx = (rng() - 0.5) * demWorldW * 0.9;
    const cy = 55 + rng() * 20;
    const cz = (rng() - 0.5) * demWorldH * 0.9;
    for (let j = 0; j < 4 + Math.floor(rng() * 4); j++) {
      const puff = new THREE.Mesh(geo, mat.clone());
      puff.material.opacity = 0.06 + rng() * 0.10;
      const s = 3 + rng() * 6;
      puff.scale.set(s * 1.5, s * 0.15, s * 1.0);
      puff.position.set(cx + (rng() - 0.5) * s * 2, cy, cz + (rng() - 0.5) * s * 1.5);
      group.add(puff);
    }
  }
  scene.add(group);
}
