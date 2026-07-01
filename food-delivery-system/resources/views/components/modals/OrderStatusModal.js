/**
 * KY Food Delivery System
 * Component: OrderStatusModal
 *
 * Displays order status with timeline and delivery information.
 *
 * @param {Object} options
 * @param {string} [options.orderId] - Order ID
 * @param {string} [options.status] - Current order status
 * @param {Array} [options.timeline] - Array of status timeline events
 * @param {Object} [options.estimatedTime] - Estimated delivery time
 * @param {Object} [options.driver] - Driver information {name, phone, vehicle}
 * @param {Function} [options.onClose] - Callback when modal closes
 * @returns {HTMLDivElement}
 */

import { Badge } from '../common/Badge.js';
import { Button } from '../common/Button.js';
import { Modal } from '../common/Modal.js';

export function OrderStatusModal({
  orderId = '',
  status = 'processing',
  timeline = [],
  estimatedTime = null,
  driver = null,
  onClose = null,
} = {}) {
  const content = document.createElement('div');
  content.className = 'order-status-modal__content';

  const header = document.createElement('div');
  header.className = 'order-status-modal__header';

  const title = document.createElement('h3');
  title.className = 'order-status-modal__title';
  title.textContent = `Order #${orderId}`;
  header.appendChild(title);

  const statusBadge = Badge({
    label: status,
    variant: mapStatusToBadge(status),
  });
  statusBadge.className = 'order-status-modal__badge';
  header.appendChild(statusBadge);

  content.appendChild(header);

  if (estimatedTime) {
    const timeInfo = document.createElement('div');
    timeInfo.className = 'order-status-modal__time-info';
    timeInfo.innerHTML = `<span>Estimated delivery:</span> <strong>${estimatedTime}</strong>`;
    content.appendChild(timeInfo);
  }

  if (timeline.length > 0) {
    const timelineEl = document.createElement('div');
    timelineEl.className = 'order-status-modal__timeline';

    timeline.forEach((event, index) => {
      const step = document.createElement('div');
      step.className = 'order-status-timeline__step';
      if (index === 0) step.classList.add('order-status-timeline__step--active');

      const dot = document.createElement('div');
      dot.className = 'order-status-timeline__dot';
      step.appendChild(dot);

      const info = document.createElement('div');
      info.className = 'order-status-timeline__info';

      const eventTitle = document.createElement('h4');
      eventTitle.className = 'order-status-timeline__event-title';
      eventTitle.textContent = event.title;
      info.appendChild(eventTitle);

      const eventTime = document.createElement('span');
      eventTime.className = 'order-status-timeline__event-time';
      eventTime.textContent = event.time || '';
      info.appendChild(eventTime);

      step.appendChild(info);
      timelineEl.appendChild(step);
    });

    content.appendChild(timelineEl);
  }

  if (driver) {
    const driverSection = document.createElement('div');
    driverSection.className = 'order-status-modal__driver';

    const driverTitle = document.createElement('h4');
    driverTitle.className = 'order-status-modal__driver-title';
    driverTitle.textContent = 'Delivery Partner';
    driverSection.appendChild(driverTitle);

    const driverInfo = document.createElement('div');
    driverInfo.className = 'order-status-modal__driver-info';

    const driverName = document.createElement('span');
    driverName.className = 'order-status-modal__driver-name';
    driverName.textContent = driver.name;
    driverInfo.appendChild(driverName);

    if (driver.vehicle) {
      const vehicle = document.createElement('span');
      vehicle.className = 'order-status-modal__driver-vehicle';
      vehicle.textContent = driver.vehicle;
      driverInfo.appendChild(vehicle);
    }

    driverSection.appendChild(driverInfo);

    if (driver.phone) {
      const contactBtn = Button({
        label: 'Contact Driver',
        variant: 'outline',
        size: 'sm',
        onClick: () => window.location.href = `tel:${driver.phone}`,
      });
      driverSection.appendChild(contactBtn);
    }

    content.appendChild(driverSection);
  }

  const modal = Modal({
    content,
    onClose,
  });

  modal.className = 'order-status-modal';

  return modal;
}

function mapStatusToBadge(status) {
  const statusMap = {
    pending: 'warning',
    processing: 'info',
    ready: 'success',
    out_for_delivery: 'info',
    delivered: 'success',
    completed: 'success',
    cancelled: 'danger',
  };
  return statusMap[status] || 'default';
}
