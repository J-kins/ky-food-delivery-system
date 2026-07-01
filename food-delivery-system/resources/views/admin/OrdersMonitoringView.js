/**
 * KY Food Delivery System
 * Admin: Orders Monitoring
 */

export function OrdersMonitoringView() {
  const container = document.createElement('div');
  container.className = 'orders-monitoring-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Orders Monitoring';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const statusGrid = document.createElement('div');
  statusGrid.style.display = 'grid';
  statusGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(180px, 1fr))';
  statusGrid.style.gap = 'var(--spacing-lg)';
  statusGrid.style.marginBottom = 'var(--spacing-xl)';

  const statuses = [
    { name: 'Pending', count: 45, color: '#E8D7B5' },
    { name: 'Confirmed', count: 102, color: '#F0C019' },
    { name: 'Preparing', count: 78, color: '#F03919' },
    { name: 'Ready', count: 34, color: '#00AB66' },
    { name: 'Delivering', count: 56, color: '#005638' },
    { name: 'Completed', count: 1248, color: '#A89F93' }
  ];

  statuses.forEach(status => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';
    card.style.borderTop = `4px solid ${status.color}`;
    card.style.textAlign = 'center';

    const name = document.createElement('p');
    name.textContent = status.name;
    name.style.margin = '0 0 var(--spacing-sm) 0';
    name.style.color = '#837A70';

    const count = document.createElement('h3');
    count.textContent = status.count;
    count.style.margin = '0';
    count.style.color = 'var(--color-neutral-brown)';

    card.appendChild(name);
    card.appendChild(count);
    statusGrid.appendChild(card);
  });

  container.appendChild(statusGrid);

  const chartSection = document.createElement('div');
  chartSection.style.backgroundColor = 'var(--color-white)';
  chartSection.style.padding = 'var(--spacing-lg)';
  chartSection.style.borderRadius = 'var(--radius-md)';

  const chartTitle = document.createElement('h2');
  chartTitle.textContent = 'Order Distribution';
  chartTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const canvas = document.createElement('canvas');
  canvas.id = 'order-distribution-chart';
  canvas.style.width = '100%';
  canvas.style.height = '400px';

  chartSection.appendChild(chartTitle);
  chartSection.appendChild(canvas);
  container.appendChild(chartSection);

  return container;
}
