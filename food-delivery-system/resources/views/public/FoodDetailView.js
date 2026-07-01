/**
 * KY Food Delivery System
 * View: Food Detail
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';
import { Input } from '../components/common/Input.js';

export function FoodDetailView() {
  const container = document.createElement('div');
  container.className = 'food-detail-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const backBtn = Button({ label: 'Back', variant: 'secondary', size: 'sm' });
  backBtn.onclick = () => window.history.back();
  container.appendChild(backBtn);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = '1fr 1fr';
  grid.style.gap = 'var(--spacing-xl)';
  grid.style.marginTop = 'var(--spacing-xl)';

  const imageSection = document.createElement('div');
  const img = document.createElement('img');
  img.src = '/resources/assets/images/placeholder/food/food-burger.jpg';
  img.alt = 'Classic Burger';
  img.style.width = '100%';
  img.style.borderRadius = 'var(--radius-lg)';
  imageSection.appendChild(img);
  grid.appendChild(imageSection);

  const details = document.createElement('div');

  const name = document.createElement('h1');
  name.textContent = 'Classic KY Burger';
  name.style.color = 'var(--color-neutral-brown)';
  name.style.marginBottom = 'var(--spacing-sm)';

  const restaurant = document.createElement('p');
  restaurant.textContent = 'KY Burger Palace';
  restaurant.style.color = 'var(--color-primary-green)';
  restaurant.style.margin = '0 0 var(--spacing-md) 0';
  restaurant.style.fontWeight = '600';

  const rating = document.createElement('div');
  rating.style.display = 'flex';
  rating.style.gap = 'var(--spacing-md)';
  rating.style.marginBottom = 'var(--spacing-lg)';
  rating.style.fontSize = '0.9375rem';

  const ratingStars = document.createElement('span');
  ratingStars.textContent = '★ 4.8';
  ratingStars.style.color = 'var(--color-primary-yellow)';

  const reviews = document.createElement('span');
  reviews.textContent = '(324 reviews)';
  reviews.style.color = '#837A70';

  rating.appendChild(ratingStars);
  rating.appendChild(reviews);

  const price = document.createElement('p');
  price.textContent = 'UGX 15,000';
  price.style.fontSize = '1.5rem';
  price.style.color = 'var(--color-primary-green)';
  price.style.fontWeight = '700';
  price.style.marginBottom = 'var(--spacing-lg)';

  const description = document.createElement('p');
  description.textContent = 'A delicious classic burger with fresh beef patty, crisp lettuce, juicy tomato, and special sauce on a toasted bun.';
  description.style.color = '#837A70';
  description.style.lineHeight = '1.6';
  description.style.marginBottom = 'var(--spacing-lg)';

  const addons = document.createElement('div');
  addons.style.marginBottom = 'var(--spacing-lg)';

  const addonsTitle = document.createElement('h3');
  addonsTitle.textContent = 'Customize';
  addonsTitle.style.color = 'var(--color-neutral-brown)';
  addonsTitle.style.marginBottom = 'var(--spacing-md)';

  const quantityLabel = document.createElement('label');
  quantityLabel.textContent = 'Quantity: ';
  quantityLabel.style.display = 'flex';
  quantityLabel.style.alignItems = 'center';
  quantityLabel.style.gap = 'var(--spacing-sm)';
  quantityLabel.style.marginBottom = 'var(--spacing-md)';

  const quantityInput = Input({
    type: 'number',
    value: '1',
    min: '1',
    max: '99'
  });
  quantityInput.style.width = '80px';

  quantityLabel.appendChild(quantityInput);

  addons.appendChild(addonsTitle);
  addons.appendChild(quantityLabel);

  const addToCartBtn = Button({
    label: 'Add to Cart',
    variant: 'primary',
    size: 'lg'
  });
  addToCartBtn.style.width = '100%';
  addToCartBtn.onclick = () => {
    const qty = quantityInput.value;
    alert(`Added ${qty} item(s) to cart!`);
    window.location.hash = '#/cart';
  };

  details.appendChild(name);
  details.appendChild(restaurant);
  details.appendChild(rating);
  details.appendChild(price);
  details.appendChild(description);
  details.appendChild(addons);
  details.appendChild(addToCartBtn);

  grid.appendChild(details);
  container.appendChild(grid);

  return container;
}
