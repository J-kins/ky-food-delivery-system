/**
 * KY Food Delivery System
 * View: Incoming Orders
 */
import { OrderList } from '../components/lists/OrderList.js';

export function IncomingOrdersView() {
  const container = document.createElement('div');
  container.className = 'incoming-orders-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const title = document.createElement('h1');
  title.textContent = 'Incoming Orders';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const orderList = OrderList({
    orders: [
      { id: '#KY12347', restaurant: 'KY Burger Palace', status: 'New', items: 'Burger x2' },
      { id: '#KY12348', restaurant: 'Pizza Haven', status: 'New', items: 'Pizza' },
      { id: '#KY12349', restaurant: 'Fresh Salad Bar', status: 'New', items: 'Salad' }
    ]
  });

  container.appendChild(orderList);
  return container;
}
