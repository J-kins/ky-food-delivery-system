/**
 * KY Food Delivery System
 * View: Delivery Status
 */
import { Card } from '../components/common/Card.js';

export function DeliveryStatusView() {
  const container = document.createElement('div');
  container.className = 'delivery-status-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '800px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Current Delivery Status';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const statusItems = [
    { step: 'Arrived at Restaurant', completed: true },
    { step: 'Order Picked Up', completed: true },
    { step: 'En Route to Customer', completed: true },
    { step: 'Arriving Soon', completed: false },
    { step: 'Delivery Complete', completed: false }
  ];

  statusItems.forEach((item, index) => {
    const content = document.createElement('div');
    content.style.display = 'flex';
    content.style.gap = 'var(--spacing-lg)';
    content.style.marginBottom = 'var(--spacing-lg)';

    const indicator = document.createElement('div');
    indicator.style.width = '40px';
    indicator.style.height = '40px';
    indicator.style.borderRadius = '50%';
    indicator.style.backgroundColor = item.completed ? 'var(--color-primary-green)' : '#E8D7B5';
    indicator.style.display = 'flex';
    indicator.style.alignItems = 'center';
    indicator.style.justifyContent = 'center';
    indicator.style.color = item.completed ? 'white' : '#837A70';
    indicator.style.fontWeight = '600';
    indicator.textContent = item.completed ? '✓' : index + 1;

    const text = document.createElement('span');
    text.textContent = item.step;
    text.style.alignSelf = 'center';
    text.style.color = item.completed ? 'var(--color-neutral-brown)' : '#837A70';

    content.appendChild(indicator);
    content.appendChild(text);

    const card = Card({ children: content, padding: 'md' });
    container.appendChild(card);
  });

  return container;
}
