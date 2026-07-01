/**
 * KY Food Delivery System
 * View: Delivery Requests
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function DeliveryRequestsView() {
  const container = document.createElement('div');
  container.className = 'delivery-requests-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Available Deliveries';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const deliveries = [
    { id: '#KY12345', from: 'KY Burger Palace', to: 'Kampala', distance: '3.2 km', earning: 'UGX 12,000' },
    { id: '#KY12346', from: 'Pizza Haven', to: 'Makerere', distance: '5.1 km', earning: 'UGX 15,000' }
  ];

  deliveries.forEach(delivery => {
    const content = document.createElement('div');

    const header = document.createElement('h3');
    header.textContent = delivery.id;
    header.style.margin = '0 0 var(--spacing-sm) 0';

    const route = document.createElement('p');
    route.textContent = `${delivery.from} → ${delivery.to}`;
    route.style.margin = '0 0 var(--spacing-sm) 0';
    route.style.color = '#837A70';

    const details = document.createElement('div');
    details.style.display = 'flex';
    details.style.gap = 'var(--spacing-lg)';
    details.style.marginBottom = 'var(--spacing-md)';

    const distanceSpan = document.createElement('span');
    distanceSpan.textContent = delivery.distance;

    const earningSpan = document.createElement('span');
    earningSpan.textContent = delivery.earning;
    earningSpan.style.fontWeight = '600';
    earningSpan.style.color = 'var(--color-primary-green)';

    details.appendChild(distanceSpan);
    details.appendChild(earningSpan);

    const acceptBtn = Button({ label: 'Accept', variant: 'primary', size: 'sm' });
    acceptBtn.onclick = () => alert('Delivery accepted! Pick up from ' + delivery.from);

    content.appendChild(header);
    content.appendChild(route);
    content.appendChild(details);
    content.appendChild(acceptBtn);

    const card = Card({ children: content, padding: 'md', hoverable: true });
    container.appendChild(card);
  });

  return container;
}
