/**
 * KY Food Delivery System
 * Component: KitchenLayout
 *
 * Layout wrapper for kitchen/restaurant staff dashboard.
 * Optimized for order queue and preparation tracking.
 *
 * @param {Object} options
 * @param {HTMLElement} options.content - Main page content
 * @param {string} [options.restaurantName] - Restaurant name
 * @param {Array} [options.stats] - Status stats {label, value, variant}
 * @returns {HTMLDivElement}
 */

export function KitchenLayout({ content, restaurantName = '', stats = [] } = {}) {
  const layout = document.createElement('div');
  layout.className = 'kitchen-layout';
  layout.style.display = 'flex';
  layout.style.flexDirection = 'column';
  layout.style.minHeight = '100vh';

  const header = document.createElement('header');
  header.className = 'kitchen-layout__header';

  const titleSection = document.createElement('div');
  titleSection.className = 'kitchen-layout__title-section';

  const title = document.createElement('h1');
  title.className = 'kitchen-layout__title';
  title.textContent = restaurantName || 'Kitchen Dashboard';
  titleSection.appendChild(title);

  header.appendChild(titleSection);

  if (stats.length > 0) {
    const statsContainer = document.createElement('div');
    statsContainer.className = 'kitchen-layout__stats';

    stats.forEach((stat) => {
      const statBox = document.createElement('div');
      statBox.className = 'kitchen-layout__stat';
      if (stat.variant) statBox.classList.add(`kitchen-layout__stat--${stat.variant}`);

      const label = document.createElement('span');
      label.className = 'kitchen-layout__stat-label';
      label.textContent = stat.label;

      const value = document.createElement('span');
      value.className = 'kitchen-layout__stat-value';
      value.textContent = stat.value;

      statBox.appendChild(value);
      statBox.appendChild(label);
      statsContainer.appendChild(statBox);
    });

    header.appendChild(statsContainer);
  }

  layout.appendChild(header);

  const body = document.createElement('div');
  body.className = 'kitchen-layout__body';
  body.style.flex = '1';
  body.style.overflowY = 'auto';

  if (content) body.appendChild(content);

  layout.appendChild(body);

  return layout;
}
