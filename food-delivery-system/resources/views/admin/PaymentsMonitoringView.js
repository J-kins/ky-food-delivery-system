/**
 * KY Food Delivery System
 * Admin: Payments Monitoring
 */

export function PaymentsMonitoringView() {
  const container = document.createElement('div');
  container.className = 'payments-monitoring-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Payments & Transactions';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const summaryGrid = document.createElement('div');
  summaryGrid.style.display = 'grid';
  summaryGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
  summaryGrid.style.gap = 'var(--spacing-lg)';
  summaryGrid.style.marginBottom = 'var(--spacing-xl)';

  const summaries = [
    { label: 'Total Revenue', amount: 'UGX 2.5B', trend: '+15%' },
    { label: 'Today', amount: 'UGX 45.2M', trend: '+8%' },
    { label: 'Pending', amount: 'UGX 2.3M', trend: '-2%' },
    { label: 'Failed', amount: 'UGX 385K', trend: '-1%' }
  ];

  summaries.forEach(summary => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';

    const label = document.createElement('p');
    label.textContent = summary.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';
    label.style.color = '#837A70';

    const amount = document.createElement('h3');
    amount.textContent = summary.amount;
    amount.style.margin = '0 0 var(--spacing-sm) 0';

    const trend = document.createElement('span');
    trend.textContent = summary.trend;
    trend.style.color = 'var(--color-primary-green)';
    trend.style.fontSize = '0.875rem';

    card.appendChild(label);
    card.appendChild(amount);
    card.appendChild(trend);
    summaryGrid.appendChild(card);
  });

  container.appendChild(summaryGrid);

  const chartContainer = document.createElement('div');
  chartContainer.style.backgroundColor = 'var(--color-white)';
  chartContainer.style.padding = 'var(--spacing-lg)';
  chartContainer.style.borderRadius = 'var(--radius-md)';

  const chartTitle = document.createElement('h2');
  chartTitle.textContent = 'Payment Methods Distribution';
  chartTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const canvas = document.createElement('canvas');
  canvas.id = 'payment-methods-chart';
  canvas.style.width = '100%';
  canvas.style.height = '350px';

  chartContainer.appendChild(chartTitle);
  chartContainer.appendChild(canvas);
  container.appendChild(chartContainer);

  return container;
}
