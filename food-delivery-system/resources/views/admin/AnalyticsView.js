/**
 * KY Food Delivery System
 * Admin: Analytics
 */

export function AnalyticsView() {
  const container = document.createElement('div');
  container.className = 'analytics-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Analytics & Reports';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const filters = document.createElement('div');
  filters.style.display = 'flex';
  filters.style.gap = 'var(--spacing-md)';
  filters.style.marginBottom = 'var(--spacing-xl)';

  const periodSelect = document.createElement('select');
  periodSelect.innerHTML = '<option>This Week</option><option>This Month</option><option>This Year</option>';
  periodSelect.style.padding = 'var(--spacing-sm) var(--spacing-md)';
  periodSelect.style.borderRadius = 'var(--radius-md)';
  periodSelect.style.border = '1px solid #D0C9BF';

  filters.appendChild(periodSelect);
  container.appendChild(filters);

  const metricsGrid = document.createElement('div');
  metricsGrid.style.display = 'grid';
  metricsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
  metricsGrid.style.gap = 'var(--spacing-lg)';

  const metrics = [
    { title: 'User Growth', chart: 'user-growth-chart' },
    { title: 'Restaurant Performance', chart: 'restaurant-perf-chart' },
    { title: 'Delivery Performance', chart: 'delivery-perf-chart' }
  ];

  metrics.forEach(metric => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';

    const header = document.createElement('h3');
    header.textContent = metric.title;
    header.style.margin = '0 0 var(--spacing-lg) 0';

    const canvas = document.createElement('canvas');
    canvas.id = metric.chart;
    canvas.style.width = '100%';
    canvas.style.height = '250px';

    card.appendChild(header);
    card.appendChild(canvas);
    metricsGrid.appendChild(card);
  });

  container.appendChild(metricsGrid);
  return container;
}
