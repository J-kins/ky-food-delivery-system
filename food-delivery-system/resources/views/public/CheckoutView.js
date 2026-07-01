/**
 * KY Food Delivery System
 * View: Checkout
 */
import { AddressForm } from '../components/forms/AddressForm.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function CheckoutView() {
  const container = document.createElement('div');
  container.className = 'checkout-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const title = document.createElement('h1');
  title.textContent = 'Checkout';
  title.style.marginBottom = 'var(--spacing-xl)';
  title.style.color = 'var(--color-neutral-brown)';
  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 380px';
  grid.style.gap = 'var(--spacing-xl)';

  const formSection = document.createElement('div');

  const addressSection = document.createElement('section');
  addressSection.style.marginBottom = 'var(--spacing-xl)';

  const addressTitle = document.createElement('h2');
  addressTitle.textContent = 'Delivery Address';
  addressTitle.style.marginBottom = 'var(--spacing-lg)';
  addressTitle.style.color = 'var(--color-neutral-brown)';

  const addressForm = AddressForm({
    onSubmit: (data) => console.log('[v0] Address:', data)
  });

  addressSection.appendChild(addressTitle);
  addressSection.appendChild(addressForm);
  formSection.appendChild(addressSection);

  const notesSection = document.createElement('section');
  const notesTitle = document.createElement('h2');
  notesTitle.textContent = 'Delivery Notes';
  notesTitle.style.marginBottom = 'var(--spacing-lg)';
  notesTitle.style.color = 'var(--color-neutral-brown)';

  const notesTextarea = document.createElement('textarea');
  notesTextarea.placeholder = 'Add special instructions for the driver...';
  notesTextarea.style.width = '100%';
  notesTextarea.style.padding = 'var(--spacing-md)';
  notesTextarea.style.borderRadius = 'var(--radius-md)';
  notesTextarea.style.border = '1.5px solid #D0C9BF';
  notesTextarea.style.fontFamily = 'Poppins, sans-serif';
  notesTextarea.style.minHeight = '100px';
  notesTextarea.style.resize = 'vertical';

  notesSection.appendChild(notesTitle);
  notesSection.appendChild(notesTextarea);
  formSection.appendChild(notesSection);

  const summary = document.createElement('div');
  const summaryCard = Card({
    children: document.createElement('div'),
    padding: 'lg'
  });

  const summaryTitle = document.createElement('h3');
  summaryTitle.textContent = 'Order Summary';
  summaryTitle.style.margin = '0 0 var(--spacing-lg) 0';
  summaryTitle.style.color = 'var(--color-neutral-brown)';

  const orderItems = document.createElement('div');
  orderItems.style.marginBottom = 'var(--spacing-lg)';
  orderItems.style.paddingBottom = 'var(--spacing-lg)';
  orderItems.style.borderBottom = '1px solid #E8D7B5';

  const itemRow = document.createElement('div');
  itemRow.style.display = 'flex';
  itemRow.style.justifyContent = 'space-between';
  itemRow.style.fontSize = '0.9375rem';
  itemRow.style.marginBottom = 'var(--spacing-sm)';

  const itemLabel = document.createElement('span');
  itemLabel.textContent = '3 items';
  itemLabel.style.color = '#837A70';

  const itemPrice = document.createElement('span');
  itemPrice.textContent = 'UGX 41,000';
  itemPrice.style.color = 'var(--color-neutral-brown)';
  itemPrice.style.fontWeight = '600';

  itemRow.appendChild(itemLabel);
  itemRow.appendChild(itemPrice);
  orderItems.appendChild(itemRow);

  const total = document.createElement('div');
  total.style.display = 'flex';
  total.style.justifyContent = 'space-between';

  const totalLabel = document.createElement('span');
  totalLabel.textContent = 'Total';
  totalLabel.style.color = 'var(--color-neutral-brown)';
  totalLabel.style.fontWeight = '600';

  const totalPrice = document.createElement('span');
  totalPrice.textContent = 'UGX 46,000';
  totalPrice.style.color = 'var(--color-primary-green)';
  totalPrice.style.fontWeight = '700';
  totalPrice.style.fontSize = '1.125rem';

  total.appendChild(totalLabel);
  total.appendChild(totalPrice);
  orderItems.appendChild(total);

  const proceedBtn = Button({
    label: 'Proceed to Payment',
    variant: 'primary',
    size: 'lg'
  });
  proceedBtn.style.width = '100%';
  proceedBtn.style.marginTop = 'var(--spacing-lg)';
  proceedBtn.onclick = () => window.location.hash = '#/payment';

  summaryCard.querySelector('div').appendChild(summaryTitle);
  summaryCard.querySelector('div').appendChild(orderItems);
  summaryCard.querySelector('div').appendChild(proceedBtn);

  summary.appendChild(summaryCard);

  grid.appendChild(formSection);
  grid.appendChild(summary);
  container.appendChild(grid);

  return container;
}
