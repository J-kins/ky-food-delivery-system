/**
 * KY Food Delivery System
 * Component: Card
 *
 * A surface container with configurable shadow, padding, and radius.
 *
 * @param {Object}      options
 * @param {HTMLElement|HTMLElement[]} [options.children] - Child elements to append
 * @param {string}      [options.shadow]     - 'none' | 'sm' | 'md' | 'lg' (default: 'md')
 * @param {string}      [options.padding]    - 'none' | 'sm' | 'md' | 'lg' (default: 'md')
 * @param {boolean}     [options.hoverable]  - Add hover lift effect
 * @param {boolean}     [options.clickable]  - Makes the card look interactive (cursor pointer)
 * @param {string}      [options.id]         - Optional id
 * @param {string}      [options.className]  - Extra CSS classes
 * @param {Function}    [options.onClick]    - Click handler
 * @returns {HTMLDivElement}
 *
 * Usage:
 *   import { Card } from './components/common/Card.js';
 *   const card = Card({ shadow: 'lg', hoverable: true, children: [titleEl, descEl] });
 */

export function Card({
  children = [],
  shadow = 'md',
  padding = 'md',
  hoverable = false,
  clickable = false,
  id = null,
  className = '',
  onClick = null,
} = {}) {
  const card = document.createElement('div');
  card.className = [
    'card',
    `card--shadow-${shadow}`,
    `card--pad-${padding}`,
    hoverable ? 'card--hoverable' : '',
    clickable ? 'card--clickable' : '',
    className,
  ].filter(Boolean).join(' ');

  if (id) card.id = id;
  if (clickable || onClick) card.style.cursor = 'pointer';
  if (onClick) card.addEventListener('click', onClick);

  // Append children
  const childArr = Array.isArray(children) ? children : [children];
  childArr.forEach((child) => {
    if (child instanceof HTMLElement) card.appendChild(child);
  });

  return card;
}
