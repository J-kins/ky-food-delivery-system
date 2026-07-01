/**
 * KY Food Delivery System
 * Component: Alert
 *
 * A dismissible notification banner.
 *
 * @param {Object}   options
 * @param {string}   options.message       - Alert message text (required)
 * @param {string}   [options.variant]     - 'success' | 'error' | 'warning' | 'info' (default: 'info')
 * @param {boolean}  [options.dismissible] - Show a close button (default: true)
 * @param {Function} [options.onDismiss]   - Callback when dismissed
 * @param {string}   [options.className]   - Extra CSS classes
 * @returns {HTMLDivElement}
 *
 * Usage:
 *   import { Alert } from './components/common/Alert.js';
 *   container.prepend(Alert({ message: 'Order placed successfully!', variant: 'success' }));
 */

const ICONS = {
  success: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>`,
  error:   `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
  warning: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  info:    `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
};

const CLOSE_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;

export function Alert({
  message = '',
  variant = 'info',
  dismissible = true,
  onDismiss = null,
  className = '',
} = {}) {
  const alert = document.createElement('div');
  alert.className = ['alert', `alert--${variant}`, className].filter(Boolean).join(' ');
  alert.setAttribute('role', 'alert');

  // Icon
  const iconWrap = document.createElement('span');
  iconWrap.className = 'alert__icon';
  iconWrap.innerHTML = ICONS[variant] || ICONS.info;
  alert.appendChild(iconWrap);

  // Message
  const msgEl = document.createElement('span');
  msgEl.className = 'alert__message';
  msgEl.textContent = message;
  alert.appendChild(msgEl);

  // Dismiss button
  if (dismissible) {
    const dismissBtn = document.createElement('button');
    dismissBtn.type = 'button';
    dismissBtn.className = 'alert__dismiss';
    dismissBtn.setAttribute('aria-label', 'Dismiss notification');
    dismissBtn.innerHTML = CLOSE_ICON;
    dismissBtn.addEventListener('click', () => {
      alert.classList.add('alert--exiting');
      alert.addEventListener('animationend', () => {
        alert.remove();
        if (onDismiss) onDismiss();
      }, { once: true });
    });
    alert.appendChild(dismissBtn);
  }

  return alert;
}
