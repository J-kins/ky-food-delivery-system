/**
 * KY Food Delivery System
 * View: Order Tracking
 */
import { OrderStatusModal } from '../components/modals/OrderStatusModal.js';

export function OrderTrackingView() {
  const container = document.createElement('div');
  container.className = 'order-tracking-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Track Order';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const modal = OrderStatusModal({
    orderId: '#KY12345',
    status: 'out_for_delivery',
    estimatedTime: '15 minutes',
    restaurant: 'KY Burger Palace',
    driver: { name: 'John Mugabe', vehicle: 'Motorcycle - UG 1234' }
  });

  container.appendChild(modal);
  return container;
}
