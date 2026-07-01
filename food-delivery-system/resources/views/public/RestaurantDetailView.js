/**
 * KY Food Delivery System
 * View: Restaurant Detail
 */
import { FoodList } from '../components/lists/FoodList.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function RestaurantDetailView() {
  const container = document.createElement('div');
  container.className = 'restaurant-detail-view';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const header = document.createElement('section');
  header.style.position = 'relative';

  const banner = document.createElement('img');
  banner.src = '/resources/assets/images/placeholder/food/food-burger.jpg';
  banner.alt = 'KY Burger Palace';
  banner.style.width = '100%';
  banner.style.height = '300px';
  banner.style.objectFit = 'cover';

  const backBtn = Button({ label: 'Back', variant: 'secondary', size: 'sm' });
  backBtn.style.position = 'absolute';
  backBtn.style.top = 'var(--spacing-lg)';
  backBtn.style.left = 'var(--spacing-lg)';
  backBtn.style.zIndex = '10';
  backBtn.onclick = () => window.location.hash = '#/restaurants';

  header.appendChild(banner);
  header.appendChild(backBtn);
  container.appendChild(header);

  const info = document.createElement('section');
  info.style.padding = 'var(--spacing-xl)';
  info.style.maxWidth = '1200px';
  info.style.margin = '0 auto';
  info.style.borderBottom = '1px solid #E8D7B5';

  const infoRow = document.createElement('div');
  infoRow.style.display = 'flex';
  infoRow.style.justifyContent = 'space-between';
  infoRow.style.alignItems = 'flex-start';
  infoRow.style.marginBottom = 'var(--spacing-lg)';

  const nameSection = document.createElement('div');
  const name = document.createElement('h1');
  name.textContent = 'KY Burger Palace';
  name.style.margin = '0 0 var(--spacing-sm) 0';
  name.style.color = 'var(--color-neutral-brown)';

  const statsRow = document.createElement('div');
  statsRow.style.display = 'flex';
  statsRow.style.gap = 'var(--spacing-lg)';
  statsRow.style.fontSize = '0.9375rem';
  statsRow.style.color = '#837A70';

  const rating = document.createElement('span');
  rating.textContent = '★ 4.8 (324 reviews)';
  rating.style.color = 'var(--color-primary-yellow)';

  const delivery = document.createElement('span');
  delivery.textContent = '25-30 min delivery';

  const minOrder = document.createElement('span');
  minOrder.textContent = 'Min order: UGX 10,000';

  statsRow.appendChild(rating);
  statsRow.appendChild(delivery);
  statsRow.appendChild(minOrder);
  nameSection.appendChild(name);
  nameSection.appendChild(statsRow);
  infoRow.appendChild(nameSection);

  const promo = document.createElement('div');
  promo.style.backgroundColor = 'var(--color-primary-yellow)';
  promo.style.padding = 'var(--spacing-md) var(--spacing-lg)';
  promo.style.borderRadius = 'var(--radius-md)';
  promo.textContent = '20% Off Your First Order';
  promo.style.color = 'var(--color-neutral-brown)';
  promo.style.fontWeight = '600';

  infoRow.appendChild(promo);
  info.appendChild(infoRow);

  const description = document.createElement('p');
  description.textContent = 'Premium burgers with fresh ingredients. Open 10 AM - 11 PM daily.';
  description.style.color = '#837A70';
  description.style.margin = '0';

  info.appendChild(description);
  container.appendChild(info);

  const menu = document.createElement('section');
  menu.style.padding = 'var(--spacing-xl)';
  menu.style.maxWidth = '1200px';
  menu.style.margin = '0 auto';

  const menuTitle = document.createElement('h2');
  menuTitle.textContent = 'Menu';
  menuTitle.style.marginBottom = 'var(--spacing-lg)';
  menuTitle.style.color = 'var(--color-neutral-brown)';
  menu.appendChild(menuTitle);

  const foodGrid = document.createElement('div');
  foodGrid.style.display = 'grid';
  foodGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(250px, 1fr))';
  foodGrid.style.gap = 'var(--spacing-lg)';

  const foods = [
    { name: 'Classic Burger', price: 'UGX 15,000' },
    { name: 'Cheese Burger', price: 'UGX 18,000' },
    { name: 'Spicy Burger', price: 'UGX 17,000' },
    { name: 'Double Burger', price: 'UGX 22,000' }
  ];

  foods.forEach(food => {
    const item = document.createElement('div');
    const title = document.createElement('h3');
    title.textContent = food.name;
    title.style.margin = '0 0 var(--spacing-sm) 0';
    title.style.color = 'var(--color-neutral-brown)';

    const price = document.createElement('p');
    price.textContent = food.price;
    price.style.color = 'var(--color-primary-green)';
    price.style.margin = '0 0 var(--spacing-md) 0';
    price.style.fontWeight = '600';

    const btn = Button({
      label: 'Add to Cart',
      variant: 'primary',
      size: 'sm'
    });
    btn.style.width = '100%';

    item.appendChild(title);
    item.appendChild(price);
    item.appendChild(btn);

    const card = Card({ children: item, padding: 'md', hoverable: true });
    foodGrid.appendChild(card);
  });

  menu.appendChild(foodGrid);
  container.appendChild(menu);

  return container;
}
