/**
 * KY Food Delivery System
 * Admin: Delivery Monitoring
 */

export function DeliveryMonitoringView() {
  const container = document.createElement('div');
  container.className = 'delivery-monitoring-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Delivery Network Monitoring';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const kpisGrid = document.createElement('div');
  kpisGrid.style.display = 'grid';
  kpisGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
  kpisGrid.style.gap = 'var(--spacing-lg)';
  kpisGrid.style.marginBottom = 'var(--spacing-xl)';

  const kpis = [
    { label: 'Active Riders', value: '245' },
    { label: 'Avg Delivery Time', value: '28 min' },
    { label: 'Completion Rate', value: '98.5%' },
    { label: 'Fleet Utilization', value: '87%' }
  ];

  kpis.forEach(kpi => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';
    card.style.textAlign = 'center';

    const label = document.createElement('p');
    label.textContent = kpi.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';
    label.style.color = '#837A70';

    const value = document.createElement('h3');
    value.textContent = kpi.value;
    value.style.margin = '0';
    value.style.color = 'var(--color-primary-green)';

    card.appendChild(label);
    card.appendChild(value);
    kpisGrid.appendChild(card);
  });

  container.appendChild(kpisGrid);

  const chartsGrid = document.createElement('div');
  chartsGrid.style.display = 'grid';
  chartsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(400px, 1fr))';
  chartsGrid.style.gap = 'var(--spacing-lg)';

  ['Delivery Performance', 'Rider Utilization'].forEach(title => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';

    const chartTitle = document.createElement('h3');
    chartTitle.textContent = title;
    chartTitle.style.margin = '0 0 var(--spacing-lg) 0';

    const canvas = document.createElement('canvas');
    canvas.id = title.toLowerCase().replace(/ /g, '-') + '-chart';
    canvas.style.width = '100%';
    canvas.style.height = '300px';

    card.appendChild(chartTitle);
    card.appendChild(canvas);
    chartsGrid.appendChild(card);
  });

  container.appendChild(chartsGrid);
  return container;
}
