/**
 * KY Food Delivery System
 * Component: DeliveryMarker
 *
 * Map marker for delivery partner location display.
 *
 * @param {Object} options
 * @param {string} [options.driverName] - Driver name
 * @param {string} [options.vehicle] - Vehicle type/info
 * @param {number} [options.rating] - Driver rating
 * @param {boolean} [options.isActive] - Whether actively delivering
 * @param {Function} [options.onMarkerClick] - Click handler
 * @returns {HTMLDivElement}
 */

export function DeliveryMarker({
  driverName = '',
  vehicle = '',
  rating = 4.8,
  isActive = true,
  onMarkerClick = null,
} = {}) {
  const marker = document.createElement('div');
  marker.className = 'delivery-marker';
  if (isActive) marker.classList.add('delivery-marker--active');

  const pin = document.createElement('div');
  pin.className = 'delivery-marker__pin';

  const icon = document.createElement('div');
  icon.className = 'delivery-marker__icon';
  icon.innerHTML = getDeliveryIcon();
  pin.appendChild(icon);

  marker.appendChild(pin);

  const popup = document.createElement('div');
  popup.className = 'delivery-marker__popup';

  if (driverName) {
    const name = document.createElement('div');
    name.className = 'delivery-marker__name';
    name.textContent = driverName;
    popup.appendChild(name);
  }

  if (vehicle) {
    const vehicleEl = document.createElement('div');
    vehicleEl.className = 'delivery-marker__vehicle';
    vehicleEl.textContent = vehicle;
    popup.appendChild(vehicleEl);
  }

  if (rating) {
    const ratingEl = document.createElement('div');
    ratingEl.className = 'delivery-marker__rating';
    ratingEl.innerHTML = `<span class="rating-stars">★</span> ${rating}`;
    popup.appendChild(ratingEl);
  }

  marker.appendChild(popup);

  if (onMarkerClick) {
    marker.style.cursor = 'pointer';
    marker.addEventListener('click', onMarkerClick);
  }

  return marker;
}

function getDeliveryIcon() {
  return `<svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 8h-1V6c0-2.76-2.24-5-5-5s-5 2.24-5 5v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6-2c1.66 0 3 1.34 3 3v2H9V6c0-1.66 1.34-3 3-3z"/>
  </svg>`;
}
