/**
 * KY Food Delivery System
 * View: Delivery Dashboard
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function DeliveryDashboardView() {
  const container = document.createElement('div');
  container.className = 'delivery-dashboard-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const title = document.createElement('h1');
  title.textContent = 'Delivery Dashboard';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const stats = document.createElement('div');
  stats.style.display = 'grid';
  stats.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
  stats.style.gap = 'var(--spacing-lg)';
  stats.style.marginBottom = 'var(--spacing-xl)';

  const statItems = [
    { label: 'Active Deliveries', value: '2' },
    { label: 'Completed Today', value: '12' },
    { label: 'Earnings Today', value: 'UGX 84,000' }
  ];

  statItems.forEach(stat => {
    const item = document.createElement('div');
    const label = document.createElement('p');
    label.textContent = stat.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';

    const value = document.createElement('h3');
    value.textContent = stat.value;
    value.style.margin = '0';
    value.style.color = 'var(--color-primary-green)';

    item.appendChild(label);
    item.appendChild(value);

    const card = Card({ children: item, padding: 'lg' });
    stats.appendChild(card);
  });

  container.appendChild(stats);

  const actionBtn = Button({ label: 'View Active Deliveries', variant: 'primary', size: 'lg' });
  actionBtn.style.width = '100%';
  actionBtn.onclick = () => window.location.hash = '#/delivery-requests';

  container.appendChild(actionBtn);
  return container;
}
