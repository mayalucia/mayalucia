// interaction.js — Hover highlight, click-to-examine, drag-to-spin.
// Theme-agnostic: delegates highlight rendering to the active theme.
//
// Hover — tooltip + resonance highlight.
// Click a crystal — camera flies close, then drag spins the crystal
//   in place (pinned at its center of mass). Scroll zooms.
// Click background or Escape — return to overview.

import * as THREE from 'three';

export function setupInteraction(ctx, meshMap, theme) {
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  const tooltip = document.getElementById('tooltip');
  const infoPanel = document.getElementById('info-panel');
  const infoLabel = document.getElementById('info-label');
  const infoDomain = document.getElementById('info-domain');
  const infoFacetTitle = document.getElementById('info-facet-title');
  const infoDesc = document.getElementById('info-desc');
  const infoStatus = document.getElementById('info-status');

  // Collect all meshes for raycasting
  const meshes = [];
  const meshToRoot = new Map();
  for (const [id, obj] of meshMap) {
    if (obj.isMesh) {
      meshes.push(obj);
      meshToRoot.set(obj, obj);
    } else {
      obj.traverse(child => {
        if (child.isMesh) {
          meshes.push(child);
          meshToRoot.set(child, obj);
        }
      });
    }
  }

  // ─── State ─────────────────────────────────────────────────────────────────

  let hoveredRoot = null;

  // Focus state
  let focusedMesh = null;
  const homePos = ctx.camera.position.clone();
  const homeTarget = ctx.controls.target.clone();

  // Animation
  let anim = null;

  // Crystal spin state
  let spinning = false;
  let spinPrevX = 0, spinPrevY = 0;

  // Facet tracking
  let currentFacetIndex = -1;
  let facetFading = false;
  const _worldNormal = new THREE.Vector3();
  const _camDir = new THREE.Vector3();

  // ─── Hover ─────────────────────────────────────────────────────────────────

  function updatePointer(event) {
    pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
    pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  }

  function raycastBody() {
    raycaster.setFromCamera(pointer, ctx.camera);
    const hits = raycaster.intersectObjects(meshes);
    if (hits.length === 0) return null;
    return meshToRoot.get(hits[0].object) || hits[0].object;
  }

  function onPointerMove(event) {
    // If spinning a crystal, rotate it
    if (spinning && focusedMesh) {
      const dx = event.clientX - spinPrevX;
      const dy = event.clientY - spinPrevY;
      if (Math.abs(dx) > 2 || Math.abs(dy) > 2) pointerMoved = true;
      spinPrevX = event.clientX;
      spinPrevY = event.clientY;

      // Rotate around camera-relative axes
      const speed = 0.008;
      const camRight = new THREE.Vector3();
      const camUp = new THREE.Vector3();
      ctx.camera.getWorldDirection(new THREE.Vector3());
      camRight.setFromMatrixColumn(ctx.camera.matrixWorld, 0);
      camUp.setFromMatrixColumn(ctx.camera.matrixWorld, 1);

      // Build rotation quaternion from screen-space drag
      const qx = new THREE.Quaternion().setFromAxisAngle(camUp, dx * speed);
      const qy = new THREE.Quaternion().setFromAxisAngle(camRight, dy * speed);
      const q = qx.multiply(qy);

      focusedMesh.quaternion.premultiply(q);

      // Sync wireframe if theme stores it
      const wire = focusedMesh.userData?._wire;
      if (wire) wire.quaternion.copy(focusedMesh.quaternion);

      return;
    }

    // Track movement for click detection (only while pointer is down)
    if (event.buttons > 0) pointerMoved = true;

    updatePointer(event);
    const root = raycastBody();

    if (root) {
      if (root !== hoveredRoot) {
        if (hoveredRoot) theme.highlightBody(hoveredRoot, false);
        hoveredRoot = root;
        theme.highlightBody(hoveredRoot, true);
        document.body.style.cursor = (focusedMesh && root === focusedMesh) ? 'grab' : 'pointer';
      }
      // Crystal active: mouse is on the focused crystal → blur text, show crystal
      if (focusedMesh && root === focusedMesh) {
        if (infoPanel) infoPanel.classList.add('crystal-active');
      }
      if (tooltip && root.userData.body && !focusedMesh) {
        tooltip.textContent = root.userData.body.label;
        tooltip.style.left = event.clientX + 12 + 'px';
        tooltip.style.top = event.clientY - 8 + 'px';
        tooltip.style.opacity = '1';
      }
    } else {
      if (hoveredRoot) theme.highlightBody(hoveredRoot, false);
      hoveredRoot = null;
      // Mouse left crystal → sharp text, dim crystal
      if (focusedMesh && infoPanel) infoPanel.classList.remove('crystal-active');
      document.body.style.cursor = 'default';
      if (tooltip) tooltip.style.opacity = '0';
    }
  }

  // ─── Pointer down/up — crystal spin or click ────────────────────────────────

  let pointerDownTime = 0;
  let pointerMoved = false;

  function onPointerDown(event) {
    pointerDownTime = performance.now();
    pointerMoved = false;

    if (!focusedMesh || anim) return;

    // Start spinning
    spinning = true;
    spinPrevX = event.clientX;
    spinPrevY = event.clientY;
    document.body.style.cursor = 'grabbing';
  }

  function onPointerUp(event) {
    const dt = performance.now() - pointerDownTime;
    const wasClick = dt < 300 && !pointerMoved;

    if (spinning) {
      spinning = false;
      document.body.style.cursor = focusedMesh ? 'grab' : 'default';
    }

    // Treat short taps without movement as clicks
    if (wasClick) {
      handleClick(event);
    }
  }

  // ─── Click logic (called from pointerUp for short taps) ───────────────────

  function handleClick(event) {
    if (anim) return;

    updatePointer(event);
    const root = raycastBody();

    if (root) {
      if (root === focusedMesh) return; // already examining this one
      focusOn(root);
    } else if (focusedMesh) {
      unfocus();
    }
  }

  function showInfo(body) {
    if (!infoPanel || !body) return;
    const [r, g, b] = body.color || [1, 1, 1];
    const hex = `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)})`;
    infoLabel.textContent = body.label || body.id;
    infoLabel.style.color = hex;
    infoDomain.textContent = body.domain || body.kind || '';
    infoStatus.textContent = body.status ? `status: ${body.status}` : '';

    // Show first facet or fall back to description
    currentFacetIndex = -1;
    const facets = body.facets;
    if (facets && facets.length > 0) {
      if (infoFacetTitle) infoFacetTitle.textContent = facets[0].title;
      infoDesc.textContent = facets[0].text;
      currentFacetIndex = 0;
    } else {
      if (infoFacetTitle) infoFacetTitle.textContent = '';
      infoDesc.textContent = body.description || '';
    }
    infoDesc.style.opacity = '1';
    infoPanel.classList.add('visible');
  }

  function hideInfo() {
    if (infoPanel) {
      infoPanel.classList.remove('visible');
      infoPanel.classList.remove('crystal-active');
    }
    currentFacetIndex = -1;
  }

  // ─── Facet detection ─────────────────────────────────────────────────────────

  function updateFacet(mesh) {
    if (!mesh) return;
    const logicalFaces = mesh.userData._logicalFaces;
    const facetMap = mesh.userData._facetMap;
    const facets = mesh.userData.body?.facets;
    if (!logicalFaces || !facetMap || !facets || facets.length === 0) return;

    // Find the face most aligned with camera view direction
    ctx.camera.getWorldDirection(_camDir);
    let bestDot = -Infinity;
    let bestFaceIdx = 0;

    for (let i = 0; i < logicalFaces.length; i++) {
      // Transform face normal by mesh quaternion to world space
      _worldNormal.copy(logicalFaces[i].normal);
      _worldNormal.applyQuaternion(mesh.quaternion);

      // Dot with negative camera direction (face pointing toward camera)
      const dot = -_worldNormal.dot(_camDir);
      if (dot > bestDot) {
        bestDot = dot;
        bestFaceIdx = i;
      }
    }

    const newFacetIdx = facetMap[bestFaceIdx];
    if (newFacetIdx === currentFacetIndex || newFacetIdx < 0 || facetFading) return;

    // Crossfade to new facet
    currentFacetIndex = newFacetIdx;
    facetFading = true;
    infoDesc.style.opacity = '0';
    if (infoFacetTitle) infoFacetTitle.style.opacity = '0';

    setTimeout(() => {
      const facet = facets[newFacetIdx];
      if (infoFacetTitle) {
        infoFacetTitle.textContent = facet.title;
        infoFacetTitle.style.opacity = '1';
      }
      infoDesc.textContent = facet.text;
      infoDesc.style.opacity = '1';
      facetFading = false;
    }, 150);
  }

  function focusOn(mesh) {
    if (focusedMesh && focusedMesh !== mesh) {
      theme.highlightBody(focusedMesh, false);
    }

    focusedMesh = mesh;
    theme.highlightBody(mesh, true);

    // Dim all other bodies
    if (theme.dimOthers) theme.dimOthers(mesh);

    const targetPos = mesh.position.clone();
    const body = mesh.userData.body;

    // Uniform visual size: all bodies subtend the same angle when focused
    if (!mesh.geometry.boundingSphere) mesh.geometry.computeBoundingSphere();
    const radius = mesh.geometry.boundingSphere.radius;
    const viewDist = radius / Math.tan(0.15);

    const dir = ctx.camera.position.clone().sub(targetPos).normalize();
    const destination = targetPos.clone().add(dir.multiplyScalar(viewDist));

    startAnimation(
      ctx.camera.position.clone(), destination,
      ctx.controls.target.clone(), targetPos,
      () => {
        ctx.controls.enabled = false;
        document.body.style.cursor = 'grab';
        showInfo(body);
        if (tooltip) tooltip.style.opacity = '0';
      }
    );
  }

  function unfocus() {
    if (focusedMesh) {
      theme.highlightBody(focusedMesh, false);
    }
    focusedMesh = null;
    spinning = false;
    hideInfo();

    // Restore all bodies
    if (theme.restoreAll) theme.restoreAll();

    startAnimation(
      ctx.camera.position.clone(), homePos.clone(),
      ctx.controls.target.clone(), homeTarget.clone(),
      () => {
        ctx.controls.enabled = true;
        document.body.style.cursor = 'default';
      }
    );
  }

  function startAnimation(from, to, fromTarget, toTarget, onComplete) {
    anim = { from, to, fromTarget, toTarget, progress: 0, onComplete };
    ctx.controls.enabled = false;
  }

  // ─── Scroll zoom while focused ─────────────────────────────────────────────

  function onWheel(event) {
    if (!focusedMesh || anim) return;

    // Zoom toward/away from the focused crystal
    const dir = ctx.camera.position.clone().sub(focusedMesh.position);
    const dist = dir.length();
    const zoomSpeed = 0.001;
    const newDist = Math.max(1.0, Math.min(15, dist + event.deltaY * zoomSpeed * dist));
    dir.normalize().multiplyScalar(newDist);
    ctx.camera.position.copy(focusedMesh.position).add(dir);
  }

  // ─── Escape key ────────────────────────────────────────────────────────────

  function onKeyDown(event) {
    if (event.key === 'Escape' && focusedMesh && !anim) {
      unfocus();
    }
  }

  // ─── Bind events ───────────────────────────────────────────────────────────

  window.addEventListener('pointermove', onPointerMove);
  window.addEventListener('pointerdown', onPointerDown);
  window.addEventListener('pointerup', onPointerUp);
  window.addEventListener('wheel', onWheel, { passive: true });
  window.addEventListener('keydown', onKeyDown);

  // ─── Per-frame update ──────────────────────────────────────────────────────

  return function onFrame() {
    // Update glyph animation time on all crystals
    const now = performance.now() * 0.001;
    for (const [, obj] of meshMap) {
      const u = obj.userData?._shaderRef?.current?.uniforms?.uTime;
      if (u) u.value = now;
    }

    // Update facet display when focused on a crystal
    if (focusedMesh && !anim) {
      updateFacet(focusedMesh);
    }

    if (!anim) return;

    anim.progress += 0.025;
    const t = easeInOut(Math.min(anim.progress, 1));

    ctx.camera.position.lerpVectors(anim.from, anim.to, t);
    const target = anim.fromTarget.clone().lerp(anim.toTarget, t);
    ctx.controls.target.copy(target);

    if (anim.progress >= 1) {
      ctx.camera.position.copy(anim.to);
      ctx.controls.target.copy(anim.toTarget);
      anim.onComplete?.();
      anim = null;
    }
  };
}

function easeInOut(t) {
  return t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(-2 * t + 2, 3) / 2;
}
