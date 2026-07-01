/**
 * KY Food Delivery System
 * Admin: Restaurants Management
 */

export function RestaurantsManagementView() {
  const container = document.createElement('div');
  container.className = 'restaurants-management-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Restaurants Management';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const table = document.createElement('table');
  table.style.width = '100%';
  table.style.borderCollapse = 'collapse';
  table.style.backgroundColor = 'var(--color-white)';
  table.style.borderRadius = 'var(--radius-md)';
  table.style.overflow = 'hidden';

  const thead = table.createTHead();
  const headerRow = thead.insertRow();
  ['Name', 'Category', 'Rating', 'Orders', 'Status'].forEach(header => {
    const th = document.createElement('th');
    th.textContent = header;
    th.style.padding = 'var(--spacing-md)';
    th.style.textAlign = 'left';
    th.style.borderBottom = '1.5px solid #D0C9BF';
    th.style.fontWeight = '600';
    headerRow.appendChild(th);
  });

  const tbody = table.createTBody();
  const restaurants = [
    { name: 'KY Burger Palace', category: 'Burgers', rating: '4.8', orders: '342', status: 'Active' },
    { name: 'Pizza Haven', category: 'Pizza', rating: '4.6', orders: '298', status: 'Active' },
    { name: 'Fresh Salad Bar', category: 'Salads', rating: '4.7', orders: '156', status: 'Active' }
  ];

  restaurants.forEach(rest => {
    const row = tbody.insertRow();
    const cells = [
      { text: rest.name, style: 'font-weight:600' },
      { text: rest.category },
      { text: rest.rating, style: 'color:var(--color-primary-green)' },
      { text: rest.orders },
      { text: rest.status, style: 'color:var(--color-primary-green)' }
    ];

    cells.forEach(cell => {
      const td = row.insertCell();
      td.textContent = cell.text;
      td.style.padding = 'var(--spacing-md)';
      td.style.borderBottom = '1px solid #E8D7B5';
      if (cell.style) td.style.cssText += ';' + cell.style;
    });
  });

  container.appendChild(table);
  return container;
}
