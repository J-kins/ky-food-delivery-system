/**
 * KY Food Delivery System
 * Component: CartItem
 *
 * Individual cart item with quantity controls and removal.
 *
 * @param {Object} options
 * @param {string} [options.id] - Item ID
 * @param {string} [options.name] - Item name
 * @param {number} [options.price] - Item price
 * @param {number} [options.quantity] - Current quantity
 * @param {string} [options.image] - Item image URL
 * @param {Function} [options.onQuantityChange] - Callback with new quantity
 * @param {Function} [options.onRemove] - Callback when removed
 * @returns {HTMLDivElement}
 */

import { Button } from './Button.js';

export function CartItem({
  id = '',
  name = '',
  price = 0,
  quantity = 1,
  image = '',
  onQuantityChange = null,
  onRemove = null,
} = {}) {
  const item = document.createElement('div');
  item.className = 'cart-item';

  const imageEl = document.createElement('div');
  imageEl.className = 'cart-item__image';
  imageEl.style.backgroundImage = `url('${image || '/resources/assets/images/placeholder/food.jpg'}')`;
  item.appendChild(imageEl);

  const content = document.createElement('div');
  content.className = 'cart-item__content';

  const nameEl = document.createElement('h4');
  nameEl.className = 'cart-item__name';
  nameEl.textContent = name;
  content.appendChild(nameEl);

  const priceEl = document.createElement('div');
  priceEl.className = 'cart-item__price';
  priceEl.textContent = `$${price.toFixed(2)}`;
  content.appendChild(priceEl);

  item.appendChild(content);

  const controls = document.createElement('div');
  controls.className = 'cart-item__controls';

  const decreaseBtn = Button({
    label: '-',
    size: 'sm',
    variant: 'outline',
    onClick: () => {
      if (quantity > 1) {
        const newQuantity = quantity - 1;
        if (onQuantityChange) onQuantityChange(id, newQuantity);
      }
    },
  });
  controls.appendChild(decreaseBtn);

  const qtyDisplay = document.createElement('span');
  qtyDisplay.className = 'cart-item__quantity';
  qtyDisplay.textContent = quantity;
  controls.appendChild(qtyDisplay);

  const increaseBtn = Button({
    label: '+',
    size: 'sm',
    variant: 'outline',
    onClick: () => {
      const newQuantity = quantity + 1;
      if (onQuantityChange) onQuantityChange(id, newQuantity);
    },
  });
  controls.appendChild(increaseBtn);

  item.appendChild(controls);

  const total = document.createElement('div');
  total.className = 'cart-item__total';
  total.textContent = `$${(price * quantity).toFixed(2)}`;
  item.appendChild(total);

  const removeBtn = Button({
    label: 'Remove',
    size: 'sm',
    variant: 'danger',
    onClick: () => {
      if (onRemove) onRemove(id);
    },
  });
  removeBtn.className = 'cart-item__remove';
  item.appendChild(removeBtn);

  return item;
}
