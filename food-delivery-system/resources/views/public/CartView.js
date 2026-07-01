/**
 * KY Food Delivery System
 * View: Cart
 */
import { CartItem } from '../components/common/CartItem.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function CartView() {
  const container = document.createElement('div');
  container.className = 'cart-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const title = document.createElement('h1');
  title.textContent = 'Your Cart';
  title.style.marginBottom = 'var(--spacing-xl)';
  title.style.color = 'var(--color-neutral-brown)';
  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 380px';
  grid.style.gap = 'var(--spacing-xl)';

  const itemsSection = document.createElement('div');

  const mockItems = [
    { name: 'Classic Burger', price: 'UGX 15,000', qty: 2 },
    { name: 'Fries', price: 'UGX 5,000', qty: 1 },
    { name: 'Soft Drink', price: 'UGX 3,000', qty: 2 }
  ];

  mockItems.forEach(item => {
    const cartItem = CartItem({
      name: item.name,
      price: item.price,
      quantity: item.qty,
      onQuantityChange: (qty) => console.log('[v0] Qty changed:', qty),
      onRemove: () => console.log('[v0] Item removed')
    });
    itemsSection.appendChild(cartItem);
  });

  const summary = document.createElement('div');
  const summaryCard = Card({
    children: document.createElement('div'),
    padding: 'lg'
  });

  const summaryTitle = document.createElement('h3');
  summaryTitle.textContent = 'Order Summary';
  summaryTitle.style.margin = '0 0 var(--spacing-lg) 0';
  summaryTitle.style.color = 'var(--color-neutral-brown)';

  const subtotal = document.createElement('div');
  subtotal.style.display = 'flex';
  subtotal.style.justifyContent = 'space-between';
  subtotal.style.marginBottom = 'var(--spacing-md)';
  subtotal.style.paddingBottom = 'var(--spacing-md)';
  subtotal.style.borderBottom = '1px solid #E8D7B5';

  const subtotalLabel = document.createElement('span');
  subtotalLabel.textContent = 'Subtotal';
  subtotalLabel.style.color = '#837A70';

  const subtotalValue = document.createElement('span');
  subtotalValue.textContent = 'UGX 41,000';
  subtotalValue.style.color = 'var(--color-neutral-brown)';
  subtotalValue.style.fontWeight = '600';

  subtotal.appendChild(subtotalLabel);
  subtotal.appendChild(subtotalValue);

  const delivery = document.createElement('div');
  delivery.style.display = 'flex';
  delivery.style.justifyContent = 'space-between';
  delivery.style.marginBottom = 'var(--spacing-lg)';
  delivery.style.paddingBottom = 'var(--spacing-lg)';
  delivery.style.borderBottom = '1px solid #E8D7B5';

  const deliveryLabel = document.createElement('span');
  deliveryLabel.textContent = 'Delivery';
  deliveryLabel.style.color = '#837A70';

  const deliveryValue = document.createElement('span');
  deliveryValue.textContent = 'UGX 5,000';
  deliveryValue.style.color = 'var(--color-neutral-brown)';
  deliveryValue.style.fontWeight = '600';

  delivery.appendChild(deliveryLabel);
  delivery.appendChild(deliveryValue);

  const total = document.createElement('div');
  total.style.display = 'flex';
  total.style.justifyContent = 'space-between';
  total.style.marginBottom = 'var(--spacing-lg)';

  const totalLabel = document.createElement('span');
  totalLabel.textContent = 'Total';
  totalLabel.style.color = 'var(--color-neutral-brown)';
  totalLabel.style.fontSize = '1.125rem';
  totalLabel.style.fontWeight = '600';

  const totalValue = document.createElement('span');
  totalValue.textContent = 'UGX 46,000';
  totalValue.style.color = 'var(--color-primary-green)';
  totalValue.style.fontSize = '1.25rem';
  totalValue.style.fontWeight = '700';

  total.appendChild(totalLabel);
  total.appendChild(totalValue);

  const checkoutBtn = Button({
    label: 'Proceed to Checkout',
    variant: 'primary',
    size: 'lg'
  });
  checkoutBtn.style.width = '100%';
  checkoutBtn.onclick = () => window.location.hash = '#/checkout';

  summaryCard.querySelector('div').appendChild(summaryTitle);
  summaryCard.querySelector('div').appendChild(subtotal);
  summaryCard.querySelector('div').appendChild(delivery);
  summaryCard.querySelector('div').appendChild(total);
  summaryCard.querySelector('div').appendChild(checkoutBtn);

  summary.appendChild(summaryCard);

  grid.appendChild(itemsSection);
  grid.appendChild(summary);
  container.appendChild(grid);

  return container;
}
