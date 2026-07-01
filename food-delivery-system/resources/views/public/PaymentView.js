/**
 * KY Food Delivery System
 * View: Payment
 */
import { PaymentForm } from '../components/forms/PaymentForm.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function PaymentView() {
  const container = document.createElement('div');
  container.className = 'payment-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '900px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const title = document.createElement('h1');
  title.textContent = 'Payment';
  title.style.marginBottom = 'var(--spacing-xl)';
  title.style.color = 'var(--color-neutral-brown)';
  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 340px';
  grid.style.gap = 'var(--spacing-xl)';

  const paymentSection = document.createElement('div');

  const paymentTitle = document.createElement('h2');
  paymentTitle.textContent = 'Payment Method';
  paymentTitle.style.marginBottom = 'var(--spacing-lg)';
  paymentTitle.style.color = 'var(--color-neutral-brown)';

  const paymentForm = PaymentForm({
    onSubmit: (data) => {
      console.log('[v0] Payment data:', data);
      alert('Payment processing...');
      setTimeout(() => {
        alert('Order confirmed! Order #KY12345');
        window.location.hash = '#/order-tracking';
      }, 1500);
    }
  });

  paymentSection.appendChild(paymentTitle);
  paymentSection.appendChild(paymentForm);

  const summary = document.createElement('div');
  const summaryCard = Card({
    children: document.createElement('div'),
    padding: 'lg'
  });

  const summaryTitle = document.createElement('h3');
  summaryTitle.textContent = 'Order Summary';
  summaryTitle.style.margin = '0 0 var(--spacing-lg) 0';
  summaryTitle.style.color = 'var(--color-neutral-brown)';

  const items = document.createElement('div');
  items.style.marginBottom = 'var(--spacing-lg)';
  items.style.paddingBottom = 'var(--spacing-lg)';
  items.style.borderBottom = '1px solid #E8D7B5';

  const itemsLabel = document.createElement('div');
  itemsLabel.style.display = 'flex';
  itemsLabel.style.justifyContent = 'space-between';
  itemsLabel.style.fontSize = '0.9375rem';
  itemsLabel.style.marginBottom = 'var(--spacing-sm)';

  const itemsLabelText = document.createElement('span');
  itemsLabelText.textContent = 'Items';
  itemsLabelText.style.color = '#837A70';

  const itemsPrice = document.createElement('span');
  itemsPrice.textContent = 'UGX 41,000';
  itemsPrice.style.color = 'var(--color-neutral-brown)';

  itemsLabel.appendChild(itemsLabelText);
  itemsLabel.appendChild(itemsPrice);

  const delivery = document.createElement('div');
  delivery.style.display = 'flex';
  delivery.style.justifyContent = 'space-between';
  delivery.style.fontSize = '0.9375rem';

  const deliveryLabel = document.createElement('span');
  deliveryLabel.textContent = 'Delivery';
  deliveryLabel.style.color = '#837A70';

  const deliveryPrice = document.createElement('span');
  deliveryPrice.textContent = 'UGX 5,000';
  deliveryPrice.style.color = 'var(--color-neutral-brown)';

  delivery.appendChild(deliveryLabel);
  delivery.appendChild(deliveryPrice);

  items.appendChild(itemsLabel);
  items.appendChild(delivery);

  const total = document.createElement('div');
  total.style.display = 'flex';
  total.style.justifyContent = 'space-between';
  total.style.marginBottom = 'var(--spacing-lg)';

  const totalLabel = document.createElement('span');
  totalLabel.textContent = 'Total';
  totalLabel.style.color = 'var(--color-neutral-brown)';
  totalLabel.style.fontWeight = '600';

  const totalPrice = document.createElement('span');
  totalPrice.textContent = 'UGX 46,000';
  totalPrice.style.color = 'var(--color-primary-green)';
  totalPrice.style.fontWeight = '700';
  totalPrice.style.fontSize = '1.25rem';

  total.appendChild(totalLabel);
  total.appendChild(totalPrice);

  summaryCard.querySelector('div').appendChild(summaryTitle);
  summaryCard.querySelector('div').appendChild(items);
  summaryCard.querySelector('div').appendChild(total);

  summary.appendChild(summaryCard);

  grid.appendChild(paymentSection);
  grid.appendChild(summary);
  container.appendChild(grid);

  return container;
}
