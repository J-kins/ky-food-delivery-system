/**
 * KY Food Delivery System
 * Component: Badge
 *
 * A small status pill/tag for displaying labels like order status or categories.
 *
 * @param {Object}  options
 * @param {string}  options.label     - Text inside the badge (required)
 * @param {string}  [options.variant] - 'default' | 'success' | 'warning' | 'danger' | 'info' | 'neutral'
 * @param {boolean} [options.dot]     - Show a leading status dot
 * @param {string}  [options.className] - Extra CSS classes
 * @returns {HTMLSpanElement}
 *
 * Usage:
 *   import { Badge } from './components/common/Badge.js';
 *   cell.appendChild(Badge({ label: 'Delivered', variant: 'success', dot: true }));
 */

export function Badge({
  label = '',
  variant = 'default',
  dot = false,
  className = '',
} = {}) {
  const badge = document.createElement('span');
  badge.className = ['badge', `badge--${variant}`, className].filter(Boolean).join(' ');
  badge.setAttribute('aria-label', `Status: ${label}`);

  if (dot) {
    const dotEl = document.createElement('span');
    dotEl.className = 'badge__dot';
    dotEl.setAttribute('aria-hidden', 'true');
    badge.appendChild(dotEl);
  }

  const text = document.createElement('span');
  text.className = 'badge__text';
  text.textContent = label;
  badge.appendChild(text);

  return badge;
}

/**
 * Map an order status string to the correct Badge variant.
 * @param {string} status
 * @returns {HTMLSpanElement}
 */
export function OrderStatusBadge(status = '') {
  const variantMap = {
    'Pending':          'warning',
    'Accepted':         'info',
    'Preparing':        'info',
    'Ready':            'success',
    'Out for Delivery': 'info',
    'Delivered':        'success',
    'Cancelled':        'danger',
  };
  const variant = variantMap[status] || 'neutral';
  return Badge({ label: status, variant, dot: true });
}
