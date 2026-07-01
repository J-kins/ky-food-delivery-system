/**
 * KY Food Delivery System
 * Component: AdminLayout
 *
 * Layout wrapper for admin dashboard pages with sidebar and header.
 *
 * @param {Object} options
 * @param {HTMLElement} options.content - Main page content
 * @param {string} [options.title] - Page title
 * @param {Array} [options.navItems] - Navigation menu items
 * @param {HTMLElement} [options.header] - Custom header element
 * @returns {HTMLDivElement}
 */

export function AdminLayout({ content, title = '', navItems = [], header = null } = {}) {
  const layout = document.createElement('div');
  layout.className = 'admin-layout';
  layout.style.display = 'flex';
  layout.style.height = '100vh';

  const sidebar = document.createElement('aside');
  sidebar.className = 'admin-layout__sidebar';

  const logo = document.createElement('div');
  logo.className = 'admin-layout__logo';
  logo.textContent = 'KY Admin';
  sidebar.appendChild(logo);

  const nav = document.createElement('nav');
  nav.className = 'admin-layout__nav';

  navItems.forEach((item) => {
    const link = document.createElement('a');
    link.href = item.href || '#';
    link.className = 'admin-layout__nav-link';
    if (item.active) link.classList.add('admin-layout__nav-link--active');
    link.textContent = item.label;
    nav.appendChild(link);
  });

  sidebar.appendChild(nav);
  layout.appendChild(sidebar);

  const main = document.createElement('main');
  main.className = 'admin-layout__main';
  main.style.flex = '1';
  main.style.display = 'flex';
  main.style.flexDirection = 'column';

  if (header) {
    main.appendChild(header);
  } else if (title) {
    const pageHeader = document.createElement('div');
    pageHeader.className = 'admin-layout__header';
    const pageTitle = document.createElement('h1');
    pageTitle.textContent = title;
    pageHeader.appendChild(pageTitle);
    main.appendChild(pageHeader);
  }

  const body = document.createElement('div');
  body.className = 'admin-layout__body';
  body.style.flex = '1';
  body.style.overflowY = 'auto';

  if (content) body.appendChild(content);

  main.appendChild(body);
  layout.appendChild(main);

  return layout;
}
