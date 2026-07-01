/**
 * KY Food Delivery System
 * View: Kitchen Queue
 */
import { Card } from '../components/common/Card.js';

export function KitchenQueueView() {
  const container = document.createElement('div');
  container.className = 'kitchen-queue-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Order Queue';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
  grid.style.gap = 'var(--spacing-lg)';

  const orders = [
    { status: 'Pending', orderId: '#KY12347', items: 'Burger x2, Fries', time: '0 min' },
    { status: 'Preparing', orderId: '#KY12346', items: 'Pizza, Salad', time: '5 min' },
    { status: 'Ready', orderId: '#KY12345', items: 'Burger, Drink', time: '10 min' }
  ];

  orders.forEach(order => {
    const content = document.createElement('div');

    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.marginBottom = 'var(--spacing-md)';

    const orderId = document.createElement('h3');
    orderId.textContent = order.orderId;
    orderId.style.margin = '0';

    const statusBadge = document.createElement('span');
    statusBadge.textContent = order.status;
    statusBadge.style.padding = '0.25rem 0.75rem';
    statusBadge.style.borderRadius = 'var(--radius-sm)';
    statusBadge.style.backgroundColor = order.status === 'Ready' ? '#00AB66' : order.status === 'Preparing' ? '#F0C019' : '#E8D7B5';
    statusBadge.style.fontSize = '0.75rem';

    header.appendChild(orderId);
    header.appendChild(statusBadge);

    const items = document.createElement('p');
    items.textContent = order.items;
    items.style.margin = '0 0 var(--spacing-sm) 0';
    items.style.color = '#837A70';

    const time = document.createElement('p');
    time.textContent = 'Time: ' + order.time;
    time.style.margin = '0';
    time.style.fontSize = '0.875rem';

    content.appendChild(header);
    content.appendChild(items);
    content.appendChild(time);

    const card = Card({ children: content, padding: 'md', hoverable: true });
    grid.appendChild(card);
  });

  container.appendChild(grid);
  return container;
}
