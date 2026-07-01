/**
 * KY Food Delivery System
 * Component: Navbar
 *
 * The main top navigation bar. Supports a logo, nav links, icon actions, and a
 * user avatar with a dropdown menu. Fully responsive — hamburger on mobile.
 *
 * @param {Object}   options
 * @param {string}   [options.logoSrc]    - Path to logo image
 * @param {string}   [options.logoAlt]    - Alt text for logo (default: 'KY Foods')
 * @param {Array}    [options.links]      - Array of { label, href, active } objects
 * @param {Object}   [options.user]       - { name, avatarSrc } or null for guest
 * @param {number}   [options.cartCount]  - Cart item count badge number
 * @param {Function} [options.onCart]     - Called when cart icon is pressed
 * @param {Function} [options.onLogout]   - Called when Logout menu item is pressed
 * @param {string}   [options.className]  - Extra CSS classes
 * @returns {HTMLElement} <nav> element
 *
 * Usage:
 *   import { Navbar } from './components/common/Navbar.js';
 *   document.body.prepend(Navbar({ links: [...], user: { name: 'Jane' }, cartCount: 3 }));
 */

import { Avatar } from './Avatar.js';

const CART_ICON   = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`;
const MENU_ICON   = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
const CLOSE_ICON  = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;
const BELL_ICON   = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`;

export function Navbar({
  logoSrc = null,
  logoAlt = 'KY Foods',
  links = [],
  user = null,
  cartCount = 0,
  onCart = null,
  onLogout = null,
  className = '',
} = {}) {
  const nav = document.createElement('nav');
  nav.className = ['navbar', className].filter(Boolean).join(' ');
  nav.setAttribute('aria-label', 'Main navigation');

  // ── Brand ──────────────────────────────────────────────────────────────────
  const brand = document.createElement('a');
  brand.href = '/';
  brand.className = 'navbar__brand';
  brand.setAttribute('aria-label', logoAlt);

  if (logoSrc) {
    const logo = document.createElement('img');
    logo.src = logoSrc;
    logo.alt = logoAlt;
    logo.className = 'navbar__logo';
    brand.appendChild(logo);
  } else {
    const wordmark = document.createElement('span');
    wordmark.className = 'navbar__wordmark';
    wordmark.textContent = logoAlt;
    brand.appendChild(wordmark);
  }
  nav.appendChild(brand);

  // ── Desktop Links ─────────────────────────────────────────────────────────
  const linkList = document.createElement('ul');
  linkList.className = 'navbar__links';
  linkList.setAttribute('role', 'list');

  links.forEach(({ label, href = '#', active = false }) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = href;
    a.textContent = label;
    a.className = ['navbar__link', active ? 'navbar__link--active' : ''].filter(Boolean).join(' ');
    if (active) a.setAttribute('aria-current', 'page');
    li.appendChild(a);
    linkList.appendChild(li);
  });

  nav.appendChild(linkList);

  // ── Actions ───────────────────────────────────────────────────────────────
  const actions = document.createElement('div');
  actions.className = 'navbar__actions';

  // Notifications
  const bellBtn = document.createElement('button');
  bellBtn.type = 'button';
  bellBtn.className = 'navbar__icon-btn';
  bellBtn.setAttribute('aria-label', 'Notifications');
  bellBtn.innerHTML = BELL_ICON;
  actions.appendChild(bellBtn);

  // Cart
  const cartBtn = document.createElement('button');
  cartBtn.type = 'button';
  cartBtn.className = 'navbar__icon-btn navbar__cart-btn';
  cartBtn.setAttribute('aria-label', cartCount > 0 ? `Cart — ${cartCount} items` : 'Cart');
  cartBtn.innerHTML = CART_ICON;
  if (cartCount > 0) {
    const badge = document.createElement('span');
    badge.className = 'navbar__cart-badge';
    badge.textContent = cartCount > 99 ? '99+' : String(cartCount);
    badge.setAttribute('aria-hidden', 'true');
    cartBtn.appendChild(badge);
  }
  if (onCart) cartBtn.addEventListener('click', onCart);
  actions.appendChild(cartBtn);

  // User avatar / dropdown
  if (user) {
    const userWrap = document.createElement('div');
    userWrap.className = 'navbar__user';

    const avatar = Avatar({
      src: user.avatarSrc || null,
      initials: user.name,
      size: 'sm',
    });
    avatar.className += ' navbar__avatar';
    avatar.setAttribute('role', 'button');
    avatar.setAttribute('tabindex', '0');
    avatar.setAttribute('aria-haspopup', 'true');
    avatar.setAttribute('aria-expanded', 'false');
    avatar.setAttribute('aria-label', `User menu for ${user.name}`);

    const dropdown = document.createElement('ul');
    dropdown.className = 'navbar__dropdown';
    dropdown.setAttribute('role', 'menu');
    dropdown.style.display = 'none';

    const dropItems = [
      { label: 'My Profile', href: '#/profile' },
      { label: 'My Orders', href: '#/orders' },
      { label: 'Settings', href: '#/settings' },
      { label: 'Logout', href: '#', danger: true, onClick: onLogout },
    ];

    dropItems.forEach(({ label, href, danger, onClick }) => {
      const li = document.createElement('li');
      li.setAttribute('role', 'menuitem');
      const a = document.createElement('a');
      a.href = href;
      a.className = ['navbar__dropdown-item', danger ? 'navbar__dropdown-item--danger' : ''].filter(Boolean).join(' ');
      a.textContent = label;
      if (onClick) {
        a.addEventListener('click', (e) => { e.preventDefault(); onClick(); });
      }
      li.appendChild(a);
      dropdown.appendChild(li);
    });

    function toggleDropdown() {
      const open = dropdown.style.display === 'none';
      dropdown.style.display = open ? 'block' : 'none';
      avatar.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    avatar.addEventListener('click', toggleDropdown);
    avatar.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleDropdown(); }
    });

    document.addEventListener('click', (e) => {
      if (!userWrap.contains(e.target)) {
        dropdown.style.display = 'none';
        avatar.setAttribute('aria-expanded', 'false');
      }
    });

    userWrap.appendChild(avatar);
    userWrap.appendChild(dropdown);
    actions.appendChild(userWrap);
  } else {
    const loginLink = document.createElement('a');
    loginLink.href = '#/login';
    loginLink.className = 'navbar__login-link';
    loginLink.textContent = 'Log in';
    actions.appendChild(loginLink);
  }

  nav.appendChild(actions);

  // ── Mobile hamburger ──────────────────────────────────────────────────────
  const hamburger = document.createElement('button');
  hamburger.type = 'button';
  hamburger.className = 'navbar__hamburger';
  hamburger.setAttribute('aria-label', 'Toggle navigation menu');
  hamburger.setAttribute('aria-expanded', 'false');
  hamburger.setAttribute('aria-controls', 'navbar-mobile-menu');
  hamburger.innerHTML = MENU_ICON;

  const mobileMenu = document.createElement('div');
  mobileMenu.id = 'navbar-mobile-menu';
  mobileMenu.className = 'navbar__mobile-menu';
  mobileMenu.style.display = 'none';

  const mobileLinks = document.createElement('ul');
  mobileLinks.setAttribute('role', 'list');
  links.forEach(({ label, href = '#', active = false }) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = href;
    a.textContent = label;
    a.className = ['navbar__mobile-link', active ? 'navbar__mobile-link--active' : ''].filter(Boolean).join(' ');
    if (active) a.setAttribute('aria-current', 'page');
    li.appendChild(a);
    mobileLinks.appendChild(li);
  });
  mobileMenu.appendChild(mobileLinks);

  hamburger.addEventListener('click', () => {
    const open = mobileMenu.style.display === 'none';
    mobileMenu.style.display = open ? 'block' : 'none';
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
    hamburger.innerHTML = open ? CLOSE_ICON : MENU_ICON;
  });

  nav.appendChild(hamburger);
  nav.appendChild(mobileMenu);

  return nav;
}
