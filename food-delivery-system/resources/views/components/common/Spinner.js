/**
 * KY Food Delivery System
 * Component: Spinner
 *
 * An accessible SVG loading spinner.
 *
 * @param {Object} options
 * @param {string} [options.size]      - 'sm' | 'md' | 'lg' (default: 'md')
 * @param {string} [options.color]     - CSS color string (default: uses --color-primary-green)
 * @param {string} [options.label]     - Screen-reader label (default: 'Loading...')
 * @param {string} [options.className] - Extra CSS classes
 * @returns {HTMLElement}
 *
 * Usage:
 *   import { Spinner } from './components/common/Spinner.js';
 *   container.appendChild(Spinner({ size: 'lg' }));
 */

export function Spinner({
  size = 'md',
  color = null,
  label = 'Loading...',
  className = '',
} = {}) {
  const wrap = document.createElement('span');
  wrap.className = ['spinner', `spinner--${size}`, className].filter(Boolean).join(' ');
  wrap.setAttribute('role', 'status');
  wrap.setAttribute('aria-label', label);

  const sizeMap = { sm: 16, md: 24, lg: 40 };
  const px = sizeMap[size] || 24;
  const strokeColor = color || 'var(--color-primary-green)';

  wrap.innerHTML = `
    <svg
      width="${px}"
      height="${px}"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      class="spinner__svg"
    >
      <circle
        cx="12" cy="12" r="10"
        stroke="currentColor"
        stroke-opacity="0.2"
        stroke-width="3"
      />
      <path
        d="M12 2a10 10 0 0 1 10 10"
        stroke="${strokeColor}"
        stroke-width="3"
        stroke-linecap="round"
      />
    </svg>
  `;

  return wrap;
}
