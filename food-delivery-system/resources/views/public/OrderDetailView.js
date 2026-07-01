/**
 * KY Food Delivery System
 * View: Order Detail
 */
import { Button } from '../components/common/Button.js';
import { Card } from '../components/common/Card.js';

export function OrderDetailView() {
  const container = document.createElement('div');
  container.className = 'order-detail-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';

  const backBtn = Button({ label: 'Back', variant: 'secondary', size: 'sm' });
  backBtn.onclick = () => window.history.back();
  container.appendChild(backBtn);

  const title = document.createElement('h1');
  title.textContent = 'Order #KY12345';
  title.style.marginTop = 'var(--spacing-lg)';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 340px';
  grid.style.gap = 'var(--spacing-xl)';

  const details = document.createElement('div');

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
    name.style.color = 'var(--color-neutral-brown)';

    const price = document.createElement('span');
    price.textContent = item.price;
    price.style.color = 'var(--color-neutral-brown)';
    price.style.fontWeight = '600';

    row.appendChild(name);
    row.appendChild(price);
    details.appendChild(row);
  });

  const summary = document.createElement('div');
  const summaryCard = Card({ children: document.createElement('div'), padding: 'lg' });

  const summaryTitle = document.createElement('h3');
  summaryTitle.textContent = 'Order Summary';
  summaryTitle.style.margin = '0 0 var(--spacing-lg) 0';

  const subtotal = document.createElement('div');
  subtotal.style.display = 'flex';
  subtotal.style.justifyContent = 'space-between';
  subtotal.style.marginBottom = 'var(--spacing-sm)';

  const subtotalLabel = document.createElement('span');
  subtotalLabel.textContent = 'Subtotal';

  const subtotalValue = document.createElement('span');
  subtotalValue.textContent = 'UGX 41,000';
  subtotalValue.style.fontWeight = '600';

  subtotal.appendChild(subtotalLabel);
  subtotal.appendChild(subtotalValue);

  const total = document.createElement('div');
  total.style.display = 'flex';
  total.style.justifyContent = 'space-between';
  total.style.fontSize = '1.125rem';

  const totalLabel = document.createElement('span');
  totalLabel.textContent = 'Total';
  totalLabel.style.fontWeight = '600';

  const totalValue = document.createElement('span');
  totalValue.textContent = 'UGX 46,000';
  totalValue.style.color = 'var(--color-primary-green)';
  totalValue.style.fontWeight = '700';

  total.appendChild(totalLabel);
  total.appendChild(totalValue);

  summaryCard.querySelector('div').appendChild(summaryTitle);
  summaryCard.querySelector('div').appendChild(subtotal);
  summaryCard.querySelector('div').appendChild(total);

  summary.appendChild(summaryCard);

  grid.appendChild(details);
  grid.appendChild(summary);
  container.appendChild(grid);

  return container;
}
