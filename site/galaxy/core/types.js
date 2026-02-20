// types.js — Shared constants and defaults for the knowledge galaxy.
// Pure data definitions. No framework dependencies.

export const KIND = {
  GALAXY_CENTER: 'galaxy-center',
  STAR: 'star',
  PLANET: 'planet',
  MOON: 'moon',
};

// Visual radius multiplier per kind
export const BASE_RADIUS = {
  [KIND.GALAXY_CENTER]: 2.0,
  [KIND.STAR]: 1.2,
  [KIND.PLANET]: 0.8,
  [KIND.MOON]: 0.4,
};

// Orbital distance multiplier per kind (from parent)
export const ORBITAL_DISTANCE = {
  [KIND.STAR]: 8.0,
  [KIND.PLANET]: 6.0,
  [KIND.MOON]: 2.5,
};

// Default placement options
export const DEFAULT_OPTIONS = {
  algorithm: 'orbital',       // 'orbital' | 'force-directed'
  goldenAngle: 2.39996323,    // radians — fibonacci spiral spacing
  tiltRange: 0.6,             // max polar tilt from equatorial plane
  forceIterations: 200,
  repulsionStrength: 50.0,
  attractionStrength: 0.1,
  damping: 0.95,
};
