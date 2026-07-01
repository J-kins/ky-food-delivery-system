/**
 * KY Food Delivery System
 * View: Home
 */
import { Button } from '../components/common/Button.js';
import { Card } from '../components/common/Card.js';

export function HomeView() {
  const container = document.createElement('div');
  container.className = 'home-view';

  // Hero Section
  const hero = document.createElement('section');
  hero.style.backgroundColor = 'var(--color-primary-green)';
  hero.style.color = 'var(--color-neutral-offwhite)';
  hero.style.padding = 'var(--spacing-xxl) var(--spacing-xl)';
  hero.style.textAlign = 'center';

  const title = document.createElement('h1');
  title.textContent = 'Bold Flavour. Fast Delivery. Always KY.';
  title.style.color = 'var(--color-white)';
  title.style.fontSize = '3rem';
  title.style.marginBottom = 'var(--spacing-md)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Order your favourite meals from KY Foods directly to your door.';
  subtitle.style.fontSize = '1.125rem';
  subtitle.style.marginBottom = 'var(--spacing-xl)';
  subtitle.style.maxWidth = '600px';
  subtitle.style.margin = '0 auto var(--spacing-xl)';

  const ctaBtn = Button({
    label: 'Order Now',
    variant: 'secondary',
    size: 'lg',
    onClick: () => window.location.hash = '#/menu'
  });

  hero.appendChild(title);
  hero.appendChild(subtitle);
  hero.appendChild(ctaBtn);
  container.appendChild(hero);

  // Featured Categories
  const featured = document.createElement('section');
  featured.style.padding = 'var(--spacing-xxl) var(--spacing-xl)';
  featured.style.maxWidth = '1200px';
  featured.style.margin = '0 auto';

  const fTitle = document.createElement('h2');
  fTitle.textContent = 'Explore Our Menu';
  fTitle.style.textAlign = 'center';
  fTitle.style.marginBottom = 'var(--spacing-xl)';
  featured.appendChild(fTitle);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(280px, 1fr))';
  grid.style.gap = 'var(--spacing-lg)';

  const categories = [
    { title: 'Burgers', img: '/resources/assets/images/placeholder/food/food-burger.jpg' },
    { title: 'Pizza', img: '/resources/assets/images/placeholder/food/food-pizza.jpg' },
    { title: 'Healthy Salads', img: '/resources/assets/images/placeholder/food/food-salad.jpg' }
  ];

  categories.forEach(cat => {
    const cardContent = document.createElement('div');
    const img = document.createElement('img');
    img.src = cat.img;
    img.alt = cat.title;
    img.style.width = '100%';
    img.style.height = '200px';
    img.style.objectFit = 'cover';
    img.style.borderRadius = 'var(--radius-md)';
    img.style.marginBottom = 'var(--spacing-sm)';

    const h3 = document.createElement('h3');
    h3.textContent = cat.title;
    h3.style.margin = '0';

    cardContent.appendChild(img);
    cardContent.appendChild(h3);

    const card = Card({
      children: cardContent,
      hoverable: true,
      clickable: true,
      onClick: () => window.location.hash = '#/menu'
    });
    grid.appendChild(card);
  });

  featured.appendChild(grid);
  container.appendChild(featured);

  return container;
}
