/**
 * KY Food Delivery System
 * Component: Button
 *
 * Factory function that creates a styled button DOM element.
 *
 * @param {Object} options
 * @param {string}  options.label      - Button text (required)
 * @param {string}  [options.variant]  - 'primary' | 'secondary' | 'outline' | 'danger' | 'text' (default: 'primary')
 * @param {string}  [options.size]     - 'sm' | 'md' | 'lg' (default: 'md')
 * @param {string}  [options.type]     - HTML button type attribute (default: 'button')
 * @param {boolean} [options.disabled] - Disabled state
 * @param {boolean} [options.loading]  - Loading state (shows spinner, disables clicks)
 * @param {string}  [options.iconSvg]  - Raw SVG string to place before the label
 * @param {string}  [options.id]       - Optional HTML id
 * @param {string}  [options.className]- Additional CSS classes
 * @param {Function}[options.onClick]  - Click handler
 * @returns {HTMLButtonElement}
 *
 * Usage:
 *   import { Button } from './components/common/Button.js';
 *   document.body.appendChild(Button({ label: 'Place Order', variant: 'primary', onClick: () => {} }));
 */

export function Button({
  label = '',
  variant = 'primary',
  size = 'md',
  type = 'button',
  disabled = false,
  loading = false,
  iconSvg = null,
  id = null,
  className = '',
  onClick = null,
} = {}) {
  const btn = document.createElement('button');
  btn.type = type;
  btn.className = ['btn', `btn--${variant}`, `btn--${size}`, className].filter(Boolean).join(' ');
  if (id) btn.id = id;

  // Disabled / loading state
  if (disabled || loading) btn.disabled = true;
  if (loading) btn.classList.add('btn--loading');

  // Icon slot
  if (iconSvg) {
    const iconWrap = document.createElement('span');
    iconWrap.className = 'btn__icon';
    iconWrap.innerHTML = iconSvg;
    btn.appendChild(iconWrap);
  }

  // Spinner (only shown when loading)
  const spinner = document.createElement('span');
  spinner.className = 'btn__spinner';
  spinner.setAttribute('aria-hidden', 'true');
  btn.appendChild(spinner);

  // Label
  const labelEl = document.createElement('span');
  labelEl.className = 'btn__label';
  labelEl.textContent = label;
  btn.appendChild(labelEl);

  if (onClick) btn.addEventListener('click', onClick);

  return btn;
}
