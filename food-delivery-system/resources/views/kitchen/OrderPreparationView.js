/**
 * KY Food Delivery System
 * View: Order Preparation
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function OrderPreparationView() {
  const container = document.createElement('div');
  container.className = 'order-preparation-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Order #KY12347 - Preparation';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const items = [
    { name: 'Classic Burger', qty: 2, status: 'In Progress' },
    { name: 'Fries', qty: 1, status: 'Completed' },
    { name: 'Soft Drink', qty: 2, status: 'Pending' }
  ];

  items.forEach(item => {
    const content = document.createElement('div');

    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.justifyContent = 'space-between';
    row.style.alignItems = 'center';
    row.style.marginBottom = 'var(--spacing-sm)';

    const name = document.createElement('h3');
    name.textContent = `${item.name} x${item.qty}`;
    name.style.margin = '0';

    const status = document.createElement('span');
    status.textContent = item.status;
    status.style.padding = '0.25rem 0.75rem';
    status.style.borderRadius = 'var(--radius-sm)';
    status.style.backgroundColor = item.status === 'Completed' ? '#00AB66' : item.status === 'In Progress' ? '#F0C019' : '#E8D7B5';
    status.style.fontSize = '0.75rem';
    status.style.color = item.status === 'Completed' ? 'white' : 'var(--color-neutral-brown)';

    row.appendChild(name);
    row.appendChild(status);
    content.appendChild(row);

    const card = Card({ children: content, padding: 'md' });
    container.appendChild(card);
  });

  const markReadyBtn = Button({ label: 'Mark as Ready', variant: 'primary', size: 'lg' });
  markReadyBtn.style.width = '100%';
  markReadyBtn.style.marginTop = 'var(--spacing-lg)';
  markReadyBtn.onclick = () => alert('Order marked as ready for pickup!');

  container.appendChild(markReadyBtn);
  return container;
}
