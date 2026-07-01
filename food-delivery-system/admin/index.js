/**
 * KY Food Delivery — Admin Portal Entry
 * Routes: #/ = Dashboard, #/orders, #/users, #/restaurants, #/settings
 */

function createPortalPage(title, description, color = '#005638') {
  const app = document.getElementById('app');
  app.innerHTML = '';

  const wrap = document.createElement('div');
  wrap.style.cssText = 'display:flex;min-height:100vh;font-family:Poppins,sans-serif;';

  // Sidebar
  const sidebar = document.createElement('nav');
  sidebar.style.cssText = `width:260px;background:${color};color:#fff;padding:24px 0;flex-shrink:0;`;
  const logo = document.createElement('div');
  logo.style.cssText = 'padding:0 24px 32px;font-family:"Baloo 2",sans-serif;font-size:22px;font-weight:700;color:#F0C019;';
  logo.textContent = 'KY FOODS — ADMIN';
  sidebar.appendChild(logo);

  const navItems = [
    { label: 'Dashboard', hash: '#/' },
    { label: 'Orders',    hash: '#/orders' },
    { label: 'Users',     hash: '#/users' },
    { label: 'Restaurants', hash: '#/restaurants' },
    { label: 'Settings',  hash: '#/settings' },
  ];
  navItems.forEach(item => {
    const a = document.createElement('a');
    a.href = item.hash;
    a.textContent = item.label;
    const active = (window.location.hash || '#/') === item.hash;
    a.style.cssText = `display:block;padding:14px 24px;color:${active ? '#F0C019' : '#E8D7B5'};text-decoration:none;font-weight:${active ? '600' : '400'};background:${active ? 'rgba(255,255,255,0.1)' : 'none'};border-left:3px solid ${active ? '#F0C019' : 'transparent'};`;
    sidebar.appendChild(a);
  });

  // Main
  const main = document.createElement('main');
  main.style.cssText = 'flex:1;background:#F7F4EF;padding:40px;';

  const h1 = document.createElement('h1');
  h1.textContent = title;
  h1.style.cssText = 'font-family:"Baloo 2",sans-serif;font-size:2rem;color:#3B2A1A;margin:0 0 8px;';

  const p = document.createElement('p');
  p.textContent = description;
  p.style.cssText = 'color:#A89F93;margin:0 0 40px;';

  // KPI cards
  const kpiRow = document.createElement('div');
  kpiRow.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:40px;';
  [['Total Orders','1,284','#005638'],['Active Users','3,920','#F03919'],['Restaurants','47','#F0C019'],['Revenue','UGX 4.2M','#3B2A1A']].forEach(([label, val, col]) => {
    const card = document.createElement('div');
    card.style.cssText = 'background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(59,42,26,0.07);';
    card.innerHTML = `<div style="font-size:13px;color:#A89F93;margin-bottom:8px;font-weight:500;">${label}</div><div style="font-size:2rem;font-weight:700;color:${col};font-family:'Baloo 2',sans-serif;">${val}</div>`;
    kpiRow.appendChild(card);
  });

  main.appendChild(h1);
  main.appendChild(p);
  main.appendChild(kpiRow);

  wrap.appendChild(sidebar);
  wrap.appendChild(main);
  app.appendChild(wrap);
}

function render() {
  const hash = window.location.hash || '#/';
  const pages = {
    '#/'            : ['Dashboard',   'Overview of system activity.'],
    '#/orders'      : ['Orders',      'Manage and monitor all orders.'],
    '#/users'       : ['Users',       'Manage system users.'],
    '#/restaurants' : ['Restaurants', 'Manage restaurant partners.'],
    '#/settings'    : ['Settings',    'System configuration and roles.'],
  };
  const [title, desc] = pages[hash] || pages['#/'];
  createPortalPage(title, desc);
}

window.addEventListener('hashchange', render);
document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', render)
  : render();
