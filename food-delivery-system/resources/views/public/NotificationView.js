/**
 * KY Food Delivery System
 * View: Notifications
 */
import { NotificationList } from '../components/lists/NotificationList.js';

export function NotificationView() {
  const container = document.createElement('div');
  container.className = 'notification-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Notifications';
  title.style.marginBottom = 'var(--spacing-lg)';

  container.appendChild(title);

  const notifList = NotificationList({
    notifications: [
      { title: 'Order Delivered', message: 'Your order #KY12345 has been delivered', time: '2 hours ago' },
      { title: 'Special Offer', message: '20% off on KY Burger Palace', time: '1 day ago' },
      { title: 'Order Confirmed', message: 'Your order #KY12344 has been confirmed', time: '3 days ago' }
    ]
  });

  container.appendChild(notifList);
  return container;
}
