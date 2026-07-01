/**
 * KY Food Delivery System
 * Component: MapComponent
 *
 * Map container for delivery tracking and location display.
 * Can integrate with external mapping libraries (Leaflet, Google Maps, etc.)
 *
 * @param {Object} options
 * @param {number} [options.latitude] - Center latitude
 * @param {number} [options.longitude] - Center longitude
 * @param {Array} [options.markers] - Array of marker objects {lat, lng, title, type}
 * @param {Function} [options.onMarkerClick] - Callback when marker is clicked
 * @returns {HTMLDivElement}
 */

export function MapComponent({
  latitude = 40.7128,
  longitude = -74.0060,
  markers = [],
  onMarkerClick = null,
} = {}) {
  const container = document.createElement('div');
  container.className = 'map-component';

  const mapArea = document.createElement('div');
  mapArea.className = 'map-component__area';
  mapArea.style.width = '100%';
  mapArea.style.height = '100%';
  mapArea.style.position = 'relative';
  mapArea.style.backgroundColor = '#E8E6E1';

  const mapPlaceholder = document.createElement('div');
  mapPlaceholder.className = 'map-component__placeholder';
  mapPlaceholder.style.width = '100%';
  mapPlaceholder.style.height = '100%';
  mapPlaceholder.style.display = 'flex';
  mapPlaceholder.style.alignItems = 'center';
  mapPlaceholder.style.justifyContent = 'center';
  mapPlaceholder.style.color = '#837A70';
  mapPlaceholder.textContent = 'Map placeholder - Integrate with Leaflet/Google Maps';

  mapArea.appendChild(mapPlaceholder);

  const markersLayer = document.createElement('div');
  markersLayer.className = 'map-component__markers';
  markersLayer.style.position = 'absolute';
  markersLayer.style.inset = '0';

  markers.forEach((marker) => {
    const markerEl = document.createElement('div');
    markerEl.className = 'map-marker';
    if (marker.type) markerEl.classList.add(`map-marker--${marker.type}`);

    const pin = document.createElement('div');
    pin.className = 'map-marker__pin';
    markerEl.appendChild(pin);

    const tooltip = document.createElement('div');
    tooltip.className = 'map-marker__tooltip';
    tooltip.textContent = marker.title || 'Location';
    markerEl.appendChild(tooltip);

    markerEl.style.position = 'absolute';
    markerEl.style.cursor = 'pointer';
    markerEl.style.left = `${Math.random() * 80 + 10}%`;
    markerEl.style.top = `${Math.random() * 80 + 10}%`;
    markerEl.style.transform = 'translate(-50%, -50%)';

    markerEl.addEventListener('click', () => {
      if (onMarkerClick) onMarkerClick(marker);
    });

    markersLayer.appendChild(markerEl);
  });

  mapArea.appendChild(markersLayer);
  container.appendChild(mapArea);

  return container;
}
