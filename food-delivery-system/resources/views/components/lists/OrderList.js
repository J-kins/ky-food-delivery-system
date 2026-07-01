/**
 * KY Food Delivery System
 * Component: OrderList
 *
 * Renders a list of orders with status, total, and action buttons.
 *
 * @param {Object} options
 * @param {Array} [options.orders] - Array of order objects with id, status, total, items, date, etc.
 * @param {Function} [options.onOrderClick] - Callback when an order is clicked
 * @param {Function} [options.onReorder] - Callback for reorder action
 * @returns {HTMLDivElement}
 */

import { Badge } from '../common/Badge.js';
import { Button } from '../common/Button.js';

export function OrderList({ orders = [], onOrderClick = null, onReorder = null } = {}) {
  const container = document.createElement('div');
  container.className = 'order-list';

  if (orders.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'order-list__empty';
    empty.textContent = 'No orders yet';
    container.appendChild(empty);
    return container;
  }

  orders.forEach((order) => {
    const item = document.createElement('div');
    item.className = 'order-item';

    const header = document.createElement('div');
    header.className = 'order-item__header';

    const info = document.createElement('div');
    info.className = 'order-item__info';

    const id = document.createElement('span');
    id.className = 'order-item__id';
    id.textContent = `Order #${order.id}`;
    info.appendChild(id);

    const date = document.createElement('span');
    date.className = 'order-item__date';
    date.textContent = order.date || new Date().toLocaleDateString();
    info.appendChild(date);

    header.appendChild(info);

    const statusBadge = Badge({
      label: order.status || 'pending',
      variant: mapStatusToBadgeVariant(order.status),
    });
    statusBadge.className = 'order-item__status';
    header.appendChild(statusBadge);

    item.appendChild(header);

    const body = document.createElement('div');
    body.className = 'order-item__body';

    const items = document.createElement('div');
    items.className = 'order-item__items';
    items.innerHTML = `<span>${order.itemCount || 0} items</span>`;
    body.appendChild(items);

    const total = document.createElement('div');
    total.className = 'order-item__total';
    total.textContent = `Total: $${(order.total || 0).toFixed(2)}`;
    body.appendChild(total);

    item.appendChild(body);

    const footer = document.createElement('div');
    footer.className = 'order-item__footer';

    const viewBtn = Button({
      label: 'View Details',
      variant: 'outline',
      size: 'sm',
      onClick: () => {
        if (onOrderClick) onOrderClick(order.id);
      },
    });
    footer.appendChild(viewBtn);

    if (order.status === 'delivered' || order.status === 'completed') {
      const reorderBtn = Button({
        label: 'Reorder',
        variant: 'text',
        size: 'sm',
        onClick: () => {
          if (onReorder) onReorder(order.id);
        },
      });
      footer.appendChild(reorderBtn);
    }

    item.appendChild(footer);
    container.appendChild(item);
  });

  return container;
}

function mapStatusToBadgeVariant(status) {
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
