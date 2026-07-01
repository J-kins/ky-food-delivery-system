/**
 * KY Food Delivery System
 * Admin: Dashboard with D3.js Analytics
 */

export function AdminDashboardView() {
  const container = document.createElement('div');
  container.className = 'admin-dashboard-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'System Dashboard';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const statsGrid = document.createElement('div');
  statsGrid.style.display = 'grid';
  statsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(250px, 1fr))';
  statsGrid.style.gap = 'var(--spacing-lg)';
  statsGrid.style.marginBottom = 'var(--spacing-xl)';

  const stats = [
    { label: 'Total Users', value: '12,450', trend: '+5.2%' },
    { label: 'Active Orders', value: '342', trend: '+12.8%' },
    { label: 'Revenue (Today)', value: 'UGX 45.2M', trend: '+8.3%' },
    { label: 'Restaurants', value: '87', trend: '+2.1%' }
  ];

  stats.forEach(stat => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';
    card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';

    const label = document.createElement('p');
    label.textContent = stat.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';
    label.style.color = '#837A70';

    const value = document.createElement('h3');
    value.textContent = stat.value;
    value.style.margin = '0 0 var(--spacing-sm) 0';
    value.style.color = 'var(--color-neutral-brown)';

    const trend = document.createElement('span');
    trend.textContent = stat.trend;
    trend.style.color = 'var(--color-primary-green)';
    trend.style.fontWeight = '600';
    trend.style.fontSize = '0.875rem';

    card.appendChild(label);
    card.appendChild(value);
    card.appendChild(trend);
    statsGrid.appendChild(card);
  });

  container.appendChild(statsGrid);

  const chartsSection = document.createElement('div');
  chartsSection.style.display = 'grid';
  chartsSection.style.gridTemplateColumns = 'repeat(auto-fit, minmax(400px, 1fr))';
  chartsSection.style.gap = 'var(--spacing-lg)';

  const revenueChart = document.createElement('div');
  revenueChart.style.backgroundColor = 'var(--color-white)';
  revenueChart.style.padding = 'var(--spacing-lg)';
  revenueChart.style.borderRadius = 'var(--radius-md)';

  const revenueTitle = document.createElement('h2');
  revenueTitle.textContent = 'Revenue Trend';
  revenueTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const revenueCanvas = document.createElement('canvas');
  revenueCanvas.id = 'revenue-chart';
  revenueCanvas.style.width = '100%';
  revenueCanvas.style.height = '300px';

  revenueChart.appendChild(revenueTitle);
  revenueChart.appendChild(revenueCanvas);
  chartsSection.appendChild(revenueChart);

  const ordersChart = document.createElement('div');
  ordersChart.style.backgroundColor = 'var(--color-white)';
  ordersChart.style.padding = 'var(--spacing-lg)';
  ordersChart.style.borderRadius = 'var(--radius-md)';

  const ordersTitle = document.createElement('h2');
  ordersTitle.textContent = 'Orders by Status';
  ordersTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const ordersCanvas = document.createElement('canvas');
  ordersCanvas.id = 'orders-chart';
  ordersCanvas.style.width = '100%';
  ordersCanvas.style.height = '300px';

  ordersChart.appendChild(ordersTitle);
  ordersChart.appendChild(ordersCanvas);
  chartsSection.appendChild(ordersChart);

  container.appendChild(chartsSection);

  return container;
}
