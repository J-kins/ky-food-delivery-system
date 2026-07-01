/**
 * KY Food Delivery System
 * Component: Rating
 *
 * A 5-star rating display or interactive selector.
 *
 * @param {Object}   options
 * @param {number}   [options.value]      - Current rating value 0-5 (default: 0). Supports halves.
 * @param {number}   [options.max]        - Max stars (default: 5)
 * @param {boolean}  [options.interactive]- Allow the user to click to set rating
 * @param {boolean}  [options.showLabel]  - Show numeric label alongside stars
 * @param {string}   [options.size]       - 'sm' | 'md' | 'lg' (default: 'md')
 * @param {string}   [options.className]  - Extra CSS classes
 * @param {Function} [options.onChange]   - Called with new value when user clicks (interactive only)
 * @returns {HTMLDivElement}
 *
 * Usage:
 *   import { Rating } from './components/common/Rating.js';
 *   card.appendChild(Rating({ value: 4.5, showLabel: true }));
 */

const STAR_FULL  = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`;
const STAR_EMPTY = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`;

export function Rating({
  value = 0,
  max = 5,
  interactive = false,
  showLabel = false,
  size = 'md',
  className = '',
  onChange = null,
} = {}) {
  const wrap = document.createElement('div');
  wrap.className = ['rating', `rating--${size}`, interactive ? 'rating--interactive' : '', className].filter(Boolean).join(' ');
  wrap.setAttribute('role', interactive ? 'radiogroup' : 'img');
  wrap.setAttribute('aria-label', `Rating: ${value} out of ${max} stars`);

  const stars = [];

  for (let i = 1; i <= max; i++) {
    const star = document.createElement('span');
    star.className = 'rating__star';
    star.innerHTML = i <= value ? STAR_FULL : STAR_EMPTY;

    if (i <= value) {
      star.classList.add('rating__star--filled');
    }

    if (interactive) {
      star.setAttribute('role', 'radio');
      star.setAttribute('aria-checked', i === value ? 'true' : 'false');
      star.setAttribute('tabindex', '0');
      star.setAttribute('aria-label', `${i} star${i > 1 ? 's' : ''}`);

      star.addEventListener('click', () => {
        stars.forEach((s, idx) => {
          const filled = idx < i;
          s.innerHTML = filled ? STAR_FULL : STAR_EMPTY;
          s.classList.toggle('rating__star--filled', filled);
          s.setAttribute('aria-checked', idx + 1 === i ? 'true' : 'false');
        });
        wrap.setAttribute('aria-label', `Rating: ${i} out of ${max} stars`);
        if (onChange) onChange(i);
      });

      star.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          star.click();
        }
      });
    }

    wrap.appendChild(star);
    stars.push(star);
  }

  if (showLabel) {
    const label = document.createElement('span');
    label.className = 'rating__label';
    label.textContent = value.toFixed(1);
    wrap.appendChild(label);
  }

  return wrap;
}
