/**
 * KY Food Delivery System
 * Component: Avatar
 *
 * Displays a user profile image with a fallback to initials.
 *
 * @param {Object}  options
 * @param {string}  [options.src]       - Image URL
 * @param {string}  [options.alt]       - Alt text for the image
 * @param {string}  [options.initials]  - Fallback initials (e.g. 'JK') shown if no src
 * @param {string}  [options.size]      - 'xs' | 'sm' | 'md' | 'lg' | 'xl' (default: 'md')
 * @param {boolean} [options.online]    - Show green online indicator dot
 * @param {string}  [options.className] - Extra CSS classes
 * @returns {HTMLDivElement}
 *
 * Usage:
 *   import { Avatar } from './components/common/Avatar.js';
 *   nav.appendChild(Avatar({ src: '/path/to/img.jpg', alt: 'Jane K.', size: 'sm', online: true }));
 */

export function Avatar({
  src = null,
  alt = 'User avatar',
  initials = '',
  size = 'md',
  online = false,
  className = '',
} = {}) {
  const wrap = document.createElement('div');
  wrap.className = ['avatar', `avatar--${size}`, online ? 'avatar--online' : '', className].filter(Boolean).join(' ');

  if (src) {
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.className = 'avatar__img';
    img.loading = 'lazy';
    img.addEventListener('error', () => {
      img.replaceWith(makeInitialsEl(initials || alt));
    });
    wrap.appendChild(img);
  } else {
    wrap.appendChild(makeInitialsEl(initials || alt));
  }

  if (online) {
    const dot = document.createElement('span');
    dot.className = 'avatar__online-dot';
    dot.setAttribute('aria-label', 'Online');
    wrap.appendChild(dot);
  }

  return wrap;
}

function makeInitialsEl(text) {
  const span = document.createElement('span');
  span.className = 'avatar__initials';
  // Take first letters of up to first two words
  const words = text.trim().split(/\s+/).slice(0, 2);
  span.textContent = words.map((w) => w[0].toUpperCase()).join('');
  return span;
}
