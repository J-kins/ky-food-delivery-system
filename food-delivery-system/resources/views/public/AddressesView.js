/**
 * KY Food Delivery System
 * View: Addresses
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function AddressesView() {
  const container = document.createElement('div');
  container.className = 'addresses-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'My Addresses';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gap = 'var(--spacing-lg)';

  const addresses = [
    { type: 'Home', address: '123 Main St, Kampala', phone: '+256 700 123456' },
    { type: 'Work', address: '456 Business Ave, Kampala', phone: '+256 700 654321' }
  ];

  addresses.forEach(addr => {
    const content = document.createElement('div');
    
    const label = document.createElement('h3');
    label.textContent = addr.type;
    label.style.margin = '0 0 var(--spacing-sm) 0';

    const address = document.createElement('p');
    address.textContent = addr.address;
    address.style.margin = '0 0 var(--spacing-sm) 0';
    address.style.color = '#837A70';

    const phone = document.createElement('p');
    phone.textContent = addr.phone;
    phone.style.margin = '0';
    phone.style.color = '#837A70';

    content.appendChild(label);
    content.appendChild(address);
    content.appendChild(phone);

    const card = Card({ children: content, padding: 'lg', hoverable: true });
    grid.appendChild(card);
  });

  container.appendChild(grid);
  return container;
}
