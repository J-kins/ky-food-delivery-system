/**
 * KY Food Delivery System
 * View: Delivery Detail
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function DeliveryDetailView() {
  const container = document.createElement('div');
  container.className = 'delivery-detail-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Delivery #KY12345';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 1fr';
  grid.style.gap = 'var(--spacing-lg)';

  const orderSection = document.createElement('div');
  const orderTitle = document.createElement('h2');
  orderTitle.textContent = 'Order Items';
  orderTitle.style.marginBottom = 'var(--spacing-lg)';

  const items = [
    { name: 'Classic Burger x2', price: 'UGX 30,000' },
    { name: 'Fries', price: 'UGX 5,000' },
    { name: 'Soft Drink x2', price: 'UGX 6,000' }
  ];

  items.forEach(item => {
    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.justifyContent = 'space-between';
    row.style.padding = 'var(--spacing-sm) 0';
    row.style.borderBottom = '1px solid #E8D7B5';

    const name = document.createElement('span');
    name.textContent = item.name;

    const price = document.createElement('span');
    price.textContent = item.price;
    price.style.fontWeight = '600';

    row.appendChild(name);
    row.appendChild(price);
    orderSection.appendChild(row);
  });

  orderSection.appendChild(orderTitle);
  grid.appendChild(orderSection);

  const customerSection = document.createElement('div');
  const customerTitle = document.createElement('h2');
  customerTitle.textContent = 'Customer Info';
  customerTitle.style.marginBottom = 'var(--spacing-lg)';

  const customerInfo = document.createElement('div');
  customerInfo.style.display = 'flex';
  customerInfo.style.flexDirection = 'column';
  customerInfo.style.gap = 'var(--spacing-sm)';

  const customerName = document.createElement('p');
  customerName.textContent = 'John Doe';
  customerName.style.margin = '0';
  customerName.style.fontWeight = '600';

  const customerPhone = document.createElement('p');
  customerPhone.textContent = '+256 700 123456';
  customerPhone.style.margin = '0';
  customerPhone.style.color = '#837A70';

  const customerAddress = document.createElement('p');
  customerAddress.textContent = 'Kampala, Uganda';
  customerAddress.style.margin = '0';
  customerAddress.style.color = '#837A70';

  customerInfo.appendChild(customerName);
  customerInfo.appendChild(customerPhone);
  customerInfo.appendChild(customerAddress);

  customerSection.appendChild(customerTitle);
  customerSection.appendChild(customerInfo);
  grid.appendChild(customerSection);

  container.appendChild(grid);
  return container;
}
