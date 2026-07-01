/**
 * KY Food Delivery System
 * Component: NotificationList
 *
 * Renders a list of notifications with timestamps, types, and dismiss actions.
 *
 * @param {Object} options
 * @param {Array} [options.notifications] - Array of notification objects with id, type, message, timestamp, etc.
 * @param {Function} [options.onDismiss] - Callback when a notification is dismissed
 * @param {Function} [options.onNotificationClick] - Callback when a notification is clicked
 * @returns {HTMLDivElement}
 */

import { Badge } from '../common/Badge.js';

export function NotificationList({
  notifications = [],
  onDismiss = null,
  onNotificationClick = null,
} = {}) {
  const container = document.createElement('div');
  container.className = 'notification-list';

  if (notifications.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'notification-list__empty';
    empty.textContent = 'No notifications';
    container.appendChild(empty);
    return container;
  }

  notifications.forEach((notif) => {
    const item = document.createElement('div');
    item.className = 'notification-item';
    if (!notif.read) item.classList.add('notification-item--unread');

    const icon = document.createElement('div');
    icon.className = 'notification-item__icon';
    icon.innerHTML = getNotificationIcon(notif.type);
    item.appendChild(icon);

    const content = document.createElement('div');
    content.className = 'notification-item__content';

    const message = document.createElement('div');
    message.className = 'notification-item__message';
    message.textContent = notif.message;
    content.appendChild(message);

    const timestamp = document.createElement('div');
    timestamp.className = 'notification-item__timestamp';
    timestamp.textContent = formatTime(notif.timestamp);
    content.appendChild(timestamp);

    item.appendChild(content);

    const dismiss = document.createElement('button');
    dismiss.className = 'notification-item__dismiss';
    dismiss.setAttribute('aria-label', 'Dismiss notification');
    dismiss.innerHTML = '&times;';
    dismiss.addEventListener('click', (e) => {
      e.stopPropagation();
      if (onDismiss) onDismiss(notif.id);
    });
    item.appendChild(dismiss);

    item.style.cursor = 'pointer';
    item.addEventListener('click', () => {
      if (onNotificationClick) onNotificationClick(notif.id);
    });

    container.appendChild(item);
  });

  return container;
}

function getNotificationIcon(type) {
  const icons = {
    order: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 11l3 3L22 4"/></svg>',
    delivery: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2l9 5v6c0 5-9 8-9 8s-9-3-9-8v-6l9-5z"/></svg>',
    promotion: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M6 9h12M6 15h12"/></svg>',
    alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2l10 18H2L12 2z"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  };
  return icons[type] || icons.info;
}

function formatTime(timestamp) {
  if (!timestamp) return 'just now';
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;
  return date.toLocaleDateString();
}
