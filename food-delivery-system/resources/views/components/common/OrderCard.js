/**
 * KY Food Delivery System
 * Component: OrderCard
 *
 * Compact order card showing order summary and quick actions.
 *
 * @param {Object} options
 * @param {string} [options.id] - Order ID
 * @param {string} [options.restaurantName] - Restaurant name
 * @param {string} [options.status] - Order status
 * @param {number} [options.total] - Order total
 * @param {Array} [options.items] - Order items
 * @param {Function} [options.onView] - Callback for view action
 * @param {Function} [options.onCancel] - Callback for cancel action
 * @returns {HTMLDivElement}
 */

import { Badge } from './Badge.js';
import { Button } from './Button.js';

export function OrderCard({
  id = '',
  restaurantName = '',
  status = 'pending',
  total = 0,
  items = [],
  onView = null,
  onCancel = null,
} = {}) {
  const card = document.createElement('div');
  card.className = 'order-card';

  const header = document.createElement('div');
  header.className = 'order-card__header';

  const orderInfo = document.createElement('div');
  orderInfo.className = 'order-card__info';

  const orderId = document.createElement('h4');
  orderId.className = 'order-card__id';
  orderId.textContent = `Order #${id}`;
  orderInfo.appendChild(orderId);

  const restaurant = document.createElement('span');
  restaurant.className = 'order-card__restaurant';
  restaurant.textContent = restaurantName;
  orderInfo.appendChild(restaurant);

  header.appendChild(orderInfo);

  const statusBadge = Badge({
    label: status,
    variant: mapStatusToVariant(status),
  });
  statusBadge.className = 'order-card__status';
  header.appendChild(statusBadge);

  card.appendChild(header);

  const body = document.createElement('div');
  body.className = 'order-card__body';

  const itemsDiv = document.createElement('div');
  itemsDiv.className = 'order-card__items';
  itemsDiv.innerHTML = `<span>${items.length} items</span>`;
  body.appendChild(itemsDiv);

  const totalDiv = document.createElement('div');
  totalDiv.className = 'order-card__total';
  totalDiv.innerHTML = `Total: <strong>$${total.toFixed(2)}</strong>`;
  body.appendChild(totalDiv);

  card.appendChild(body);

  const footer = document.createElement('div');
  footer.className = 'order-card__footer';

  if (onView) {
    const viewBtn = Button({
      label: 'View',
      size: 'sm',
      variant: 'outline',
      onClick: onView,
    });
    footer.appendChild(viewBtn);
  }

  if (status === 'pending' && onCancel) {
    const cancelBtn = Button({
      label: 'Cancel',
      size: 'sm',
      variant: 'text',
      onClick: onCancel,
    });
    footer.appendChild(cancelBtn);
  }

  card.appendChild(footer);

  return card;
}

function mapStatusToVariant(status) {
  const map = {
    pending: 'warning',
    processing: 'info',
    ready: 'success',
    out_for_delivery: 'info',
    delivered: 'success',
    cancelled: 'danger',
  };
  return map[status] || 'default';
}
