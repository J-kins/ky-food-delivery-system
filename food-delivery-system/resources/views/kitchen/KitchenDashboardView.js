/**
 * KY Food Delivery System
 * View: Kitchen Dashboard
 */
import { OrderList } from '../components/lists/OrderList.js';
import { Card } from '../components/common/Card.js';

export function KitchenDashboardView() {
  const container = document.createElement('div');
  container.className = 'kitchen-dashboard-view';
  container.style.backgroundColor = '#DC4024';
  container.style.color = 'var(--color-white)';
  container.style.padding = 'var(--spacing-xl)';

  const header = document.createElement('section');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Kitchen Dashboard';
  title.style.color = 'var(--color-white)';
  title.style.margin = '0';

  header.appendChild(title);
  container.appendChild(header);

  const stats = document.createElement('div');
  stats.style.display = 'grid';
  stats.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
  stats.style.gap = 'var(--spacing-lg)';
  stats.style.marginBottom = 'var(--spacing-xl)';
  stats.style.maxWidth = '1200px';
  stats.style.margin = '0 auto var(--spacing-xl)';

  const statItems = [
    { label: 'Active Orders', value: '8' },
    { label: 'Ready for Pickup', value: '3' },
    { label: 'Completed Today', value: '24' }
  ];

  statItems.forEach(stat => {
    const item = document.createElement('div');
    item.style.backgroundColor = 'rgba(255,255,255,0.1)';
    item.style.padding = 'var(--spacing-lg)';
    item.style.borderRadius = 'var(--radius-md)';
    item.style.textAlign = 'center';

    const label = document.createElement('p');
    label.textContent = stat.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';

    const value = document.createElement('h3');
    value.textContent = stat.value;
    value.style.margin = '0';
    value.style.fontSize = '2rem';

    item.appendChild(label);
    item.appendChild(value);
    stats.appendChild(item);
  });

  container.appendChild(stats);

  const ordersSection = document.createElement('section');
  ordersSection.style.maxWidth = '1200px';
  ordersSection.style.margin = '0 auto';
  ordersSection.style.backgroundColor = 'var(--color-neutral-offwhite)';
  ordersSection.style.padding = 'var(--spacing-xl)';
  ordersSection.style.borderRadius = 'var(--radius-lg)';

  const ordersTitle = document.createElement('h2');
  ordersTitle.textContent = 'Active Orders';
  ordersTitle.style.color = 'var(--color-neutral-brown)';
  ordersTitle.style.marginBottom = 'var(--spacing-lg)';

  ordersSection.appendChild(ordersTitle);

  const orderList = OrderList({
    orders: [
      { id: '#KY12345', restaurant: 'KY Burger Palace', status: 'Preparing', items: 'Burger x2, Fries' },
      { id: '#KY12346', restaurant: 'Pizza Haven', status: 'Ready', items: 'Pizza, Salad' }
    ]
  });

  ordersSection.appendChild(orderList);
  container.appendChild(ordersSection);

  return container;
}
