/**
 * KY Food Delivery System
 * Component: PublicLayout
 *
 * Wrapper for public-facing pages, combining Navbar, main content, and Footer.
 *
 * @param {Object} options
 * @param {HTMLElement} options.content - The main page content to display
 * @returns {HTMLDivElement}
 */
import { Navbar } from '../common/Navbar.js';
import { Footer } from '../common/Footer.js';

export function PublicLayout({ content } = {}) {
  const layout = document.createElement('div');
  layout.className = 'public-layout';
  layout.style.display = 'flex';
  layout.style.flexDirection = 'column';
  layout.style.minHeight = '100vh';

  const nav = Navbar({
    logoAlt: 'KY Foods',
    links: [
      { label: 'Home', href: '#/', active: window.location.hash === '#/' || !window.location.hash },
      { label: 'Menu', href: '#/menu', active: window.location.hash.startsWith('#/menu') },
    ],
    cartCount: 2,
    onCart: () => console.log('Cart clicked'),
  });

  const main = document.createElement('main');
  main.className = 'public-layout__main';
  main.style.flex = '1';
  
  if (content) {
    main.appendChild(content);
  }

  const foot = Footer({
    columns: [
      {
        heading: 'Explore',
        links: [
          { label: 'Our Menu', href: '#/menu' },
          { label: 'Track Order', href: '#/track' },
          { label: 'Promotions', href: '#/promos' },
        ]
      },
      {
        heading: 'Legal',
        links: [
          { label: 'Terms of Service', href: '/terms' },
          { label: 'Privacy Policy', href: '/privacy' },
        ]
      }
    ]
  });

  layout.appendChild(nav);
  layout.appendChild(main);
  layout.appendChild(foot);

  return layout;
}
