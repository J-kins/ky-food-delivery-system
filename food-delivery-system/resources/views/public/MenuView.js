/**
 * KY Food Delivery System
 * View: Menu
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';
import { Badge } from '../components/common/Badge.js';

export function MenuView() {
  const container = document.createElement('div');
  container.className = 'menu-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Our Menu';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
  grid.style.gap = 'var(--spacing-xl)';

  const items = [
    { name: 'Classic KY Burger', price: 'UGX 15,000', cat: 'Burgers', img: '/resources/assets/images/placeholder/food/food-burger.jpg', popular: true },
    { name: 'Spicy Pepperoni Pizza', price: 'UGX 35,000', cat: 'Pizza', img: '/resources/assets/images/placeholder/food/food-pizza.jpg', popular: false },
    { name: 'Fresh Garden Salad', price: 'UGX 12,000', cat: 'Salads', img: '/resources/assets/images/placeholder/food/food-salad.jpg', popular: false },
    { name: 'Creamy Pasta', price: 'UGX 22,000', cat: 'Pasta', img: '/resources/assets/images/placeholder/food/food-pasta.jpg', popular: true },
    { name: 'Assorted Sushi', price: 'UGX 45,000', cat: 'Sushi', img: '/resources/assets/images/placeholder/food/food-sushi.jpg', popular: false },
    { name: 'Chocolate Lava Cake', price: 'UGX 18,000', cat: 'Desserts', img: '/resources/assets/images/placeholder/food/food-dessert.jpg', popular: true },
  ];

  items.forEach(item => {
    const content = document.createElement('div');
    content.style.display = 'flex';
    content.style.flexDirection = 'column';
    content.style.height = '100%';
    
    // Image container
    const imgWrap = document.createElement('div');
    imgWrap.style.position = 'relative';
    const img = document.createElement('img');
    img.src = item.img;
    img.alt = item.name;
    img.style.width = '100%';
    img.style.height = '200px';
    img.style.objectFit = 'cover';
    img.style.borderRadius = 'var(--radius-md)';
    img.style.marginBottom = 'var(--spacing-sm)';
    imgWrap.appendChild(img);

    if (item.popular) {
      const popularBadge = Badge({ label: 'Popular', variant: 'warning' });
      popularBadge.style.position = 'absolute';
      popularBadge.style.top = '10px';
      popularBadge.style.left = '10px';
      imgWrap.appendChild(popularBadge);
    }
    content.appendChild(imgWrap);

    // Details
    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'flex-start';
    
    const h3 = document.createElement('h3');
    h3.textContent = item.name;
    h3.style.margin = '0 0 var(--spacing-xs)';
    h3.style.fontSize = '1.125rem';
    
    const price = document.createElement('strong');
    price.textContent = item.price;
    price.style.color = 'var(--color-primary-green)';
    price.style.fontSize = '1.125rem';

    header.appendChild(h3);
    header.appendChild(price);
    content.appendChild(header);

    const desc = document.createElement('p');
    desc.textContent = `A delicious ${item.cat.toLowerCase()} prepared fresh.`;
    desc.style.fontSize = '0.875rem';
    desc.style.color = 'var(--color-neutral-brown)';
    desc.style.opacity = '0.8';
    desc.style.flex = '1';
    content.appendChild(desc);

    const addBtn = Button({
      label: 'Add to Cart',
      variant: 'primary',
      onClick: () => alert(`Added ${item.name} to cart!`)
    });
    addBtn.style.marginTop = 'var(--spacing-md)';
    content.appendChild(addBtn);

    const card = Card({ children: content, padding: 'md', hoverable: true });
    grid.appendChild(card);
  });

  container.appendChild(grid);
  return container;
}
