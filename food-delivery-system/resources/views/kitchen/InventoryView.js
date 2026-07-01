/**
 * KY Food Delivery System
 * View: Inventory
 */
import { Card } from '../components/common/Card.js';

export function InventoryView() {
  const container = document.createElement('div');
  container.className = 'inventory-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Inventory Management';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const inventory = [
    { item: 'Beef Patties', stock: 50, status: 'Normal' },
    { item: 'Bread Buns', stock: 8, status: 'Low' },
    { item: 'Fries', stock: 100, status: 'Normal' },
    { item: 'Lettuce', stock: 3, status: 'Critical' }
  ];

  inventory.forEach(inv => {
    const content = document.createElement('div');

    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.justifyContent = 'space-between';
    row.style.alignItems = 'center';
    row.style.marginBottom = 'var(--spacing-md)';

    const name = document.createElement('h3');
    name.textContent = inv.item;
    name.style.margin = '0';

    const info = document.createElement('div');
    info.style.display = 'flex';
    info.style.gap = 'var(--spacing-lg)';
    info.style.alignItems = 'center';

    const stock = document.createElement('span');
    stock.textContent = `${inv.stock} units`;
    stock.style.color = '#837A70';

    const statusBadge = document.createElement('span');
    statusBadge.textContent = inv.status;
    statusBadge.style.padding = '0.25rem 0.75rem';
    statusBadge.style.borderRadius = 'var(--radius-sm)';
    statusBadge.style.backgroundColor = inv.status === 'Normal' ? '#00AB66' : inv.status === 'Low' ? '#F0C019' : '#DC4024';
    statusBadge.style.color = 'white';
    statusBadge.style.fontSize = '0.75rem';

    info.appendChild(stock);
    info.appendChild(statusBadge);

    row.appendChild(name);
    row.appendChild(info);
    content.appendChild(row);

    const card = Card({ children: content, padding: 'md' });
    container.appendChild(card);
  });

  return container;
}
