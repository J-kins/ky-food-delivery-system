/**
 * KY Food Delivery System
 * View: Delivery Navigation
 */
import { MapComponent } from '../components/common/MapComponent.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function DeliveryNavigationView() {
  const container = document.createElement('div');
  container.className = 'delivery-navigation-view';
  container.style.display = 'grid';
  container.style.gridTemplateColumns = '1fr 300px';
  container.style.height = '100vh';
  container.style.gap = '0';

  const mapSection = document.createElement('div');

  const mapComponent = MapComponent({
    destination: 'Kampala, Uganda',
    markers: [
      { lat: 0.3476, lng: 32.5825, type: 'pickup', label: 'Pickup' },
      { lat: 0.3355, lng: 32.5898, type: 'delivery', label: 'Delivery' }
    ]
  });

  mapSection.appendChild(mapComponent);

  const sidebar = document.createElement('div');
  sidebar.style.padding = 'var(--spacing-lg)';
  sidebar.style.overflowY = 'auto';
  sidebar.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const deliveryTitle = document.createElement('h2');
  deliveryTitle.textContent = 'Order #KY12345';
  deliveryTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const details = document.createElement('div');
  details.style.marginBottom = 'var(--spacing-lg)';

  const pickupLabel = document.createElement('p');
  pickupLabel.textContent = 'Pickup';
  pickupLabel.style.fontWeight = '600';
  pickupLabel.style.margin = '0 0 var(--spacing-sm) 0';

  const pickupAddress = document.createElement('p');
  pickupAddress.textContent = 'KY Burger Palace, Main St';
  pickupAddress.style.margin = '0 0 var(--spacing-md) 0';
  pickupAddress.style.color = '#837A70';

  const deliveryLabel = document.createElement('p');
  deliveryLabel.textContent = 'Delivery';
  deliveryLabel.style.fontWeight = '600';
  deliveryLabel.style.margin = '0 0 var(--spacing-sm) 0';

  const deliveryAddress = document.createElement('p');
  deliveryAddress.textContent = 'Customer Address, Kampala';
  deliveryAddress.style.margin = '0';
  deliveryAddress.style.color = '#837A70';

  details.appendChild(pickupLabel);
  details.appendChild(pickupAddress);
  details.appendChild(deliveryLabel);
  details.appendChild(deliveryAddress);

  const completeBtn = Button({ label: 'Mark as Delivered', variant: 'primary', size: 'lg' });
  completeBtn.style.width = '100%';
  completeBtn.onclick = () => alert('Delivery completed!');

  sidebar.appendChild(deliveryTitle);
  sidebar.appendChild(details);
  sidebar.appendChild(completeBtn);

  container.appendChild(mapSection);
  container.appendChild(sidebar);

  return container;
}
