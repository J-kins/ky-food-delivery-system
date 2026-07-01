/**
 * KY Food Delivery System
 * View: Order History
 */
import { OrderList } from '../components/lists/OrderList.js';

export function OrderHistoryView() {
  const container = document.createElement('div');
  container.className = 'order-history-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Order History';
  title.style.marginBottom = 'var(--spacing-lg)';

  container.appendChild(title);
  
  const orderList = OrderList({
    orders: [
      { id: '#KY12345', restaurant: 'KY Burger Palace', amount: 'UGX 46,000', status: 'Delivered', date: '2 days ago' },
      { id: '#KY12344', restaurant: 'Pizza Haven', amount: 'UGX 52,000', status: 'Delivered', date: '5 days ago' },
      { id: '#KY12343', restaurant: 'Fresh Salad Bar', amount: 'UGX 28,000', status: 'Delivered', date: '1 week ago' }
    ]
  });

  container.appendChild(orderList);
  return container;
}
