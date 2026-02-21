// galaxy.js — Crystalline knowledge graph.
//
// Bodies are faceted polytopes — icosahedra, dodecahedra, octahedra —
// suspended in quiet space. No visible bonds. Instead, colour resonance:
// hover a crystal and its bonded partners pulse in sympathy.

import * as THREE from 'three';
import { KIND, BASE_RADIUS } from '../../core/types.js';

// Polytope assignment by kind
const POLYTOPE = {
  [KIND.GALAXY_CENTER]: (r) => new THREE.IcosahedronGeometry(r, 1),
  [KIND.STAR]:          (r) => new THREE.DodecahedronGeometry(r, 0),
  [KIND.PLANET]:        (r) => new THREE.IcosahedronGeometry(r, 0),
  [KIND.MOON]:          (r) => new THREE.OctahedronGeometry(r, 0),
};

// ─── Module state for resonance ──────────────────────────────────────────────

const meshById = new Map();       // bodyId → mesh
const bondGraph = new Map();      // bodyId → Set<{ partnerId, strength }>

function addBondEdge(fromId, toId, strength) {
  if (!bondGraph.has(fromId)) bondGraph.set(fromId, new Set());
  if (!bondGraph.has(toId)) bondGraph.set(toId, new Set());
  bondGraph.get(fromId).add({ partnerId: toId, strength });
  bondGraph.get(toId).add({ partnerId: fromId, strength });
}

// ─── Logical face extraction ─────────────────────────────────────────────────
// Cluster coplanar triangles into logical faces (e.g. 5 triangles → 1 pentagon
// for dodecahedra, 4 triangles → 1 face for subdivided icosahedra).

function extractLogicalFaces(geometry) {
  const pos = geometry.getAttribute('position');
  const triCount = pos.count / 3;
  const triangles = [];
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  const ab = new THREE.Vector3(), ac = new THREE.Vector3();

  for (let i = 0; i < pos.count; i += 3) {
    a.fromBufferAttribute(pos, i);
    b.fromBufferAttribute(pos, i + 1);
    c.fromBufferAttribute(pos, i + 2);

    const center = new THREE.Vector3().addVectors(a, b).add(c).divideScalar(3);
    ab.subVectors(b, a);
    ac.subVectors(c, a);
    const normal = new THREE.Vector3().crossVectors(ab, ac).normalize();

    triangles.push({ center: center.clone(), normal: normal.clone() });
  }

  // Cluster by normal direction (dot > 0.96 ≈ 15°)
  const used = new Array(triCount).fill(false);
  const logical = [];
  const triToFace = new Int32Array(triCount);

  for (let i = 0; i < triCount; i++) {
    if (used[i]) continue;
    used[i] = true;
    const faceIdx = logical.length;
    const clusterIndices = [i];
    triToFace[i] = faceIdx;

    for (let j = i + 1; j < triCount; j++) {
      if (used[j]) continue;
      if (triangles[i].normal.dot(triangles[j].normal) > 0.96) {
        used[j] = true;
        clusterIndices.push(j);
        triToFace[j] = faceIdx;
      }
    }

    const avgCenter = new THREE.Vector3();
    const avgNormal = new THREE.Vector3();
    for (const idx of clusterIndices) {
      avgCenter.add(triangles[idx].center);
      avgNormal.add(triangles[idx].normal);
    }
    avgCenter.divideScalar(clusterIndices.length);
    avgNormal.normalize();

    logical.push({ center: avgCenter, normal: avgNormal });
  }

  // Per-vertex attributes: faceId, face normal, face center
  // This avoids dynamic uniform array indexing in the shader.
  const vCount = pos.count;
  const faceIdArr = new Float32Array(vCount);
  const faceNormArr = new Float32Array(vCount * 3);
  const faceCentArr = new Float32Array(vCount * 3);

  for (let t = 0; t < triCount; t++) {
    const face = logical[triToFace[t]];
    for (let v = 0; v < 3; v++) {
      const idx = t * 3 + v;
      faceIdArr[idx] = triToFace[t];
      faceNormArr[idx * 3]     = face.normal.x;
      faceNormArr[idx * 3 + 1] = face.normal.y;
      faceNormArr[idx * 3 + 2] = face.normal.z;
      faceCentArr[idx * 3]     = face.center.x;
      faceCentArr[idx * 3 + 1] = face.center.y;
      faceCentArr[idx * 3 + 2] = face.center.z;
    }
  }

  geometry.setAttribute('aFaceId', new THREE.BufferAttribute(faceIdArr, 1));
  geometry.setAttribute('aFaceNormal', new THREE.BufferAttribute(faceNormArr, 3));
  geometry.setAttribute('aFaceCenter', new THREE.BufferAttribute(faceCentArr, 3));

  return logical;
}

// ─── Theme ───────────────────────────────────────────────────────────────────

export default {
  getSceneDefaults() {
    return {
      background: 0x0A0A12,
      cameraPos: [0, 6, 18],
      cameraTarget: [0, 0, 0],
      cameraNear: 0.1,
      cameraFar: 200,
      orbitMinDistance: 4,
      orbitMaxDistance: 50,
      bloomStrength: 0.25,
      bloomRadius: 0.25,
      bloomThreshold: 0.7,
    };
  },

  renderEnvironment(scene) {
    meshById.clear();
    bondGraph.clear();

    scene.add(new THREE.AmbientLight(0x303040, 0.4));

    const key = new THREE.DirectionalLight(0xCCCCEE, 0.8);
    key.position.set(5, 8, 6);
    scene.add(key);

    const fill = new THREE.DirectionalLight(0x444466, 0.25);
    fill.position.set(-3, -4, 2);
    scene.add(fill);

    const rim = new THREE.DirectionalLight(0x6666AA, 0.2);
    rim.position.set(0, 2, -10);
    scene.add(rim);

    // Sparse dust motes
    const count = 400;
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = 20 + Math.random() * 60;
      const theta = Math.acos(2 * Math.random() - 1);
      const phi = 2 * Math.PI * Math.random();
      positions[i * 3] = r * Math.sin(theta) * Math.cos(phi);
      positions[i * 3 + 1] = r * Math.sin(theta) * Math.sin(phi);
      positions[i * 3 + 2] = r * Math.cos(theta);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    scene.add(new THREE.Points(geo, new THREE.PointsMaterial({
      color: 0x445566, size: 0.08, sizeAttenuation: true, transparent: true, opacity: 0.5,
    })));
  },

  renderBody(scene, body, position) {
    const kind = body.kind || KIND.MOON;
    const radius = (BASE_RADIUS[kind] || 0.5) * (0.5 + (body.mass || 0.5) * 0.5);
    const [r, g, b] = body.color || [0.5, 0.5, 0.5];
    const color = new THREE.Color(r, g, b);

    const geoFn = POLYTOPE[kind] || POLYTOPE[KIND.MOON];
    const geometry = geoFn(radius);

    // Extract logical faces and assign per-vertex faceId attribute
    const logicalFaces = extractLogicalFaces(geometry);
    const facets = body.facets || [];
    const facetMap = logicalFaces.map((_, i) =>
      facets.length > 0 ? i % facets.length : -1
    );

    const emissiveStrength =
      kind === KIND.GALAXY_CENTER ? 0.25 :
      kind === KIND.STAR ? 0.12 :
      kind === KIND.PLANET ? 0.08 : 0.05;

    const material = new THREE.MeshStandardMaterial({
      color,
      emissive: color,
      emissiveIntensity: emissiveStrength,
      roughness: 0.15,
      metalness: 0.3,
      flatShading: true,
    });

    // Inject procedural glyph inscriptions into the shader
    const shaderRef = { current: null };

    material.onBeforeCompile = (shader) => {
      shader.uniforms.uTime = { value: 0.0 };
      shader.uniforms.uGlyphIntensity = { value: 0.35 };

      // Vertex: pass face data to fragment via varyings
      shader.vertexShader = shader.vertexShader
        .replace(
          '#include <common>',
          [
            '#include <common>',
            'attribute float aFaceId;',
            'attribute vec3 aFaceNormal;',
            'attribute vec3 aFaceCenter;',
            'varying float vFaceId;',
            'varying vec3 vFaceNorm;',
            'varying vec3 vFaceCent;',
            'varying vec3 vObjPos;',
          ].join('\n')
        )
        .replace(
          '#include <begin_vertex>',
          [
            '#include <begin_vertex>',
            'vFaceId = aFaceId;',
            'vFaceNorm = aFaceNormal;',
            'vFaceCent = aFaceCenter;',
            'vObjPos = position;',
          ].join('\n')
        );

      // Fragment: glyph functions + emissive injection
      shader.fragmentShader = shader.fragmentShader
        .replace(
          '#include <common>',
          [
            '#include <common>',
            'varying float vFaceId;',
            'varying vec3 vFaceNorm;',
            'varying vec3 vFaceCent;',
            'varying vec3 vObjPos;',
            'uniform float uTime;',
            'uniform float uGlyphIntensity;',
            '',
            'vec2 faceLocalUV(vec3 pos, vec3 center, vec3 norm) {',
            '  vec3 toPos = pos - center;',
            '  vec3 up = abs(norm.y) < 0.9 ? vec3(0.0,1.0,0.0) : vec3(1.0,0.0,0.0);',
            '  vec3 u = normalize(cross(norm, up));',
            '  vec3 v = cross(norm, u);',
            '  return vec2(dot(toPos, u), dot(toPos, v));',
            '}',
            '',
            'float glyphSpiral(vec2 uv, float t) {',
            '  float r = length(uv);',
            '  float a = atan(uv.y, uv.x);',
            '  float s = sin(a * 3.0 - r * 12.0 + t * 0.5);',
            '  float rn = sin(r * 18.0 - t * 0.3);',
            '  float m = smoothstep(0.45, 0.35, r);',
            '  return (max(s, rn) * 0.5 + 0.5) * m;',
            '}',
            '',
            'float glyphMandala(vec2 uv, float t) {',
            '  float r = length(uv);',
            '  float a = atan(uv.y, uv.x);',
            '  float sy = sin(a * 6.0 + t * 0.2) * 0.5 + 0.5;',
            '  float rn = sin(r * 20.0 - t * 0.4) * 0.5 + 0.5;',
            '  float p = sin(a * 3.0 + r * 8.0) * 0.5 + 0.5;',
            '  float m = smoothstep(0.45, 0.35, r);',
            '  return mix(rn, p, sy) * m;',
            '}',
            '',
            'float glyphCircuit(vec2 uv, float t) {',
            '  vec2 g = fract(uv * 6.0 + 0.5);',
            '  float h = smoothstep(0.48,0.50,g.y) - smoothstep(0.50,0.52,g.y);',
            '  float vl = smoothstep(0.48,0.50,g.x) - smoothstep(0.50,0.52,g.x);',
            '  float p = sin(uv.x*12.0 + uv.y*8.0 + t)*0.5+0.5;',
            '  float m = smoothstep(0.45, 0.35, length(uv));',
            '  return max(max(h,vl), p*0.3) * m;',
            '}',
            '',
            'float glyphScroll(vec2 uv, float t) {',
            '  float s1 = sin(uv.x*10.0 + sin(uv.y*6.0+t*0.3))*0.5+0.5;',
            '  float s2 = sin(uv.y*10.0 + cos(uv.x*6.0-t*0.2))*0.5+0.5;',
            '  float m = smoothstep(0.45, 0.35, length(uv));',
            '  return s1 * s2 * m;',
            '}',
            '',
            'float glyphConcentric(vec2 uv, float t) {',
            '  float r = length(uv);',
            '  float rn = sin(r*25.0 - t*0.5)*0.5+0.5;',
            '  float c = abs(sin(atan(uv.y,uv.x)*4.0))*0.3;',
            '  float m = smoothstep(0.45, 0.35, r);',
            '  return max(rn, c) * m;',
            '}',
            '',
            'float selectGlyph(vec2 uv, int id, float t) {',
            '  int g = id - (id / 5) * 5;',
            '  if (g == 0) return glyphSpiral(uv, t);',
            '  if (g == 1) return glyphMandala(uv, t);',
            '  if (g == 2) return glyphCircuit(uv, t);',
            '  if (g == 3) return glyphScroll(uv, t);',
            '  return glyphConcentric(uv, t);',
            '}',
          ].join('\n')
        )
        .replace(
          '#include <emissivemap_fragment>',
          [
            '#include <emissivemap_fragment>',
            '{',
            '  vec2 fuv = faceLocalUV(vObjPos, vFaceCent, vFaceNorm);',
            '  int fid = int(vFaceId + 0.5);',
            '  float gv = selectGlyph(fuv, fid, uTime);',
            '  gv = smoothstep(0.55, 0.85, gv);',
            '  // Subtle etch: slight darkening in grooves, gentle brightening on lines',
            '  float etch = mix(1.0 - uGlyphIntensity * 0.15, 1.0 + uGlyphIntensity * 0.2, gv);',
            '  totalEmissiveRadiance *= etch;',
            '}',
          ].join('\n')
        );

      shaderRef.current = shader;
    };

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(position.x, position.y, position.z);
    mesh.rotation.set(
      Math.random() * Math.PI,
      Math.random() * Math.PI,
      Math.random() * Math.PI * 0.5,
    );

    mesh.userData = {
      bodyId: body.id, body, baseEmissive: emissiveStrength,
      _logicalFaces: logicalFaces,
      _facetMap: facetMap,
      _shaderRef: shaderRef,
    };
    scene.add(mesh);

    // Register for resonance
    meshById.set(body.id, mesh);

    // Point light only for center
    if (kind === KIND.GALAXY_CENTER) {
      const light = new THREE.PointLight(color, 1.5, 25);
      light.position.copy(mesh.position);
      scene.add(light);
    }

    // Wireframe overlay for crystal edge definition
    const wire = new THREE.LineSegments(
      new THREE.WireframeGeometry(geometry),
      new THREE.LineBasicMaterial({
        color,
        transparent: true,
        opacity: kind === KIND.GALAXY_CENTER ? 0.4 : 0.2,
      })
    );
    wire.position.copy(mesh.position);
    wire.rotation.copy(mesh.rotation);
    mesh.userData._wire = wire;
    scene.add(wire);

    return mesh;
  },

  renderBond(scene, bond, fromPos, toPos, fromBody, toBody) {
    // No visible bond. Just register the relationship for resonance.
    addBondEdge(bond.from, bond.to, bond.strength || 0.5);

    // Return an invisible placeholder (interaction.js expects a return)
    const geo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(), new THREE.Vector3(),
    ]);
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({ visible: false }));
    scene.add(line);
    return line;
  },

  // Dim all bodies except the focused one
  dimOthers(focusedMesh) {
    for (const [id, mesh] of meshById) {
      if (mesh === focusedMesh) continue;
      mesh.material.transparent = true;
      mesh.material.opacity = 0.08;
      mesh.material.emissiveIntensity = 0.01;
      const wire = mesh.userData?._wire;
      if (wire) wire.material.opacity = 0.03;
    }
  },

  // Restore all bodies to normal
  restoreAll() {
    for (const [id, mesh] of meshById) {
      mesh.material.transparent = false;
      mesh.material.opacity = 1.0;
      const base = mesh.userData?.baseEmissive || 0.1;
      mesh.material.emissiveIntensity = base;
      mesh.material.roughness = 0.15;
      const wire = mesh.userData?._wire;
      if (wire) wire.material.opacity = 0.2;
    }
  },

  highlightBody(mesh, active) {
    if (!mesh?.material) return;
    const id = mesh.userData?.bodyId;
    const base = mesh.userData?.baseEmissive || 0.1;

    // Highlight the hovered crystal
    mesh.material.emissiveIntensity = active ? base * 2.0 : base;
    mesh.material.roughness = active ? 0.05 : 0.15;

    // Wireframe brightens on hover
    const wire = mesh.userData?._wire;
    if (wire) {
      wire.material.opacity = active ? 0.6 : 0.2;
    }

    // Resonance: bonded partners pulse sympathetically
    if (!id) return;
    const bonds = bondGraph.get(id);
    if (!bonds) return;

    for (const { partnerId, strength } of bonds) {
      const partner = meshById.get(partnerId);
      if (!partner?.material) continue;
      const partnerBase = partner.userData?.baseEmissive || 0.1;

      if (active) {
        // Sympathetic glow — proportional to bond strength
        partner.material.emissiveIntensity = partnerBase + strength * 0.8;
        partner.material.roughness = 0.10;
        const partnerWire = partner.userData?._wire;
        if (partnerWire) partnerWire.material.opacity = 0.15 + strength * 0.3;
      } else {
        // Restore
        partner.material.emissiveIntensity = partnerBase;
        partner.material.roughness = 0.15;
        const partnerWire = partner.userData?._wire;
        if (partnerWire) partnerWire.material.opacity = 0.2;
      }
    }
  },
};
