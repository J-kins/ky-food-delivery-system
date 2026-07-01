/**
 * KY Food Delivery — Router
 * Thin wrapper around hash-based navigation.
 */
export function navigate(hash) {
  window.location.hash = hash;
}

export function currentRoute() {
  return window.location.hash || '#/';
}
