/**
 * KY Food Delivery System
 * Component: DeliveryLayout
 *
 * Layout wrapper for delivery partner dashboard.
 * Includes map area, order list, and driver stats.
 *
 * @param {Object} options
 * @param {HTMLElement} options.mapContent - Map component or content
 * @param {HTMLElement} options.orderContent - Orders list/detail content
 * @param {Object} [options.driver] - Driver info {name, rating, earnings}
 * @returns {HTMLDivElement}
 */

export function DeliveryLayout({ mapContent, orderContent, driver = null } = {}) {
  const layout = document.createElement('div');
  layout.className = 'delivery-layout';
  layout.style.display = 'grid';
  layout.style.gridTemplateColumns = '1fr 350px';
  layout.style.height = '100vh';
  layout.style.gap = 'var(--spacing-md)';
  layout.style.padding = 'var(--spacing-md)';

  const mapContainer = document.createElement('div');
  mapContainer.className = 'delivery-layout__map';
  mapContainer.style.borderRadius = 'var(--radius-lg)';
  mapContainer.style.overflow = 'hidden';
  mapContainer.style.boxShadow = 'var(--shadow-md)';

  if (mapContent) mapContainer.appendChild(mapContent);

  layout.appendChild(mapContainer);

  const sidebar = document.createElement('aside');
  sidebar.className = 'delivery-layout__sidebar';
  sidebar.style.display = 'flex';
  sidebar.style.flexDirection = 'column';
  sidebar.style.gap = 'var(--spacing-md)';

  if (driver) {
    const driverCard = document.createElement('div');
    driverCard.className = 'delivery-layout__driver-card';

    const driverName = document.createElement('h3');
    driverName.textContent = driver.name;
    driverCard.appendChild(driverName);

    const driverRating = document.createElement('div');
    driverRating.innerHTML = `Rating: <strong>${driver.rating || 4.8}</strong>`;
    driverCard.appendChild(driverRating);

    if (driver.earnings) {
      const earnings = document.createElement('div');
      earnings.innerHTML = `Today's Earnings: <strong>$${driver.earnings}</strong>`;
      driverCard.appendChild(earnings);
    }

    sidebar.appendChild(driverCard);
  }

  const ordersContainer = document.createElement('div');
  ordersContainer.className = 'delivery-layout__orders';
  ordersContainer.style.flex = '1';
  ordersContainer.style.overflowY = 'auto';
  ordersContainer.style.borderRadius = 'var(--radius-lg)';
  ordersContainer.style.border = '1px solid #E8D7B5';

  if (orderContent) ordersContainer.appendChild(orderContent);

  sidebar.appendChild(ordersContainer);
  layout.appendChild(sidebar);

  return layout;
}
