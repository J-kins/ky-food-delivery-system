/**
 * KY Food Delivery System
 * Manager: Dashboard
 */

export function ManagerDashboardView() {
  const container = document.createElement('div');
  container.className = 'manager-dashboard-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Restaurant Dashboard';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const statsGrid = document.createElement('div');
  statsGrid.style.display = 'grid';
  statsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(220px, 1fr))';
  statsGrid.style.gap = 'var(--spacing-lg)';
  statsGrid.style.marginBottom = 'var(--spacing-xl)';

  const stats = [
    { label: 'Today Orders', value: '42', color: 'var(--color-primary-green)' },
    { label: 'Revenue', value: 'UGX 1.2M', color: 'var(--color-primary-orange)' },
    { label: 'Avg Rating', value: '4.8', color: var(--color-primary-yellow)' },
    { label: 'Active Menu Items', value: '87', color: 'var(--color-primary-orange)' }
  ];

  stats.forEach(stat => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';
    card.style.borderLeft = `4px solid ${stat.color}`;

    const label = document.createElement('p');
    label.textContent = stat.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';
    label.style.color = '#837A70';

    const value = document.createElement('h3');
    value.textContent = stat.value;
    value.style.margin = '0';
    value.style.color = 'var(--color-neutral-brown)';

    card.appendChild(label);
    card.appendChild(value);
    statsGrid.appendChild(card);
  });

  container.appendChild(statsGrid);

  const chartsGrid = document.createElement('div');
  chartsGrid.style.display = 'grid';
  chartsGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(400px, 1fr))';
  chartsGrid.style.gap = 'var(--spacing-lg)';

  ['Sales Today', 'Popular Items'].forEach(title => {
    const card = document.createElement('div');
    card.style.backgroundColor = 'var(--color-white)';
    card.style.padding = 'var(--spacing-lg)';
    card.style.borderRadius = 'var(--radius-md)';

    const chartTitle = document.createElement('h2');
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
