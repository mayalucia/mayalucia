// graph.js — Pure graph traversal helpers over the knowledge graph.
// No framework dependencies. Operates on the JSON data model.

// Build a lookup map: id → body object
export function indexBodies(bodies) {
  const map = new Map();
  for (const b of bodies) map.set(b.id, b);
  return map;
}

// Return ids of root-level bodies (those not listed as anyone's child)
export function findRoots(bodies) {
  const childSet = new Set();
  for (const b of bodies) {
    if (b.children) {
      for (const c of b.children) childSet.add(c);
    }
  }
  return bodies.filter(b => !childSet.has(b.id)).map(b => b.id);
}

// Return the parent id for a given body id, or null if root
export function findParent(bodies, id) {
  for (const b of bodies) {
    if (b.children && b.children.includes(id)) return b.id;
  }
  return null;
}

// Return bonds involving a given body id
export function bondsFor(bonds, id) {
  return bonds.filter(b => b.from === id || b.to === id);
}

// Depth-first traversal yielding { id, depth, parentId }
export function* walkTree(bodies, rootId, depth = 0) {
  const index = indexBodies(bodies);
  const root = index.get(rootId);
  if (!root) return;
  yield { id: rootId, depth, parentId: null };
  if (root.children) {
    for (const childId of root.children) {
      yield* _walkChildren(index, childId, rootId, depth + 1);
    }
  }
}

function* _walkChildren(index, id, parentId, depth) {
  const node = index.get(id);
  if (!node) return;
  yield { id, depth, parentId };
  if (node.children) {
    for (const childId of node.children) {
      yield* _walkChildren(index, childId, id, depth + 1);
    }
  }
}
