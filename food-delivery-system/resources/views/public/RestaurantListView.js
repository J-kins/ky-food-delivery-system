/**
 * KY Food Delivery System
 * View: Restaurant List
 */
import { SearchFilter } from '../components/common/SearchFilter.js';
import { Card } from '../components/common/Card.js';

export function RestaurantListView() {
  const container = document.createElement('div');
  container.className = 'restaurant-list-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const header = document.createElement('section');
  header.style.marginBottom = 'var(--spacing-xl)';
  header.style.maxWidth = '1200px';
  header.style.margin = '0 auto var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Browse Restaurants';
  title.style.color = 'var(--color-neutral-brown)';
  title.style.marginBottom = 'var(--spacing-md)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Discover your next favorite meal from our partner restaurants';
  subtitle.style.color = '#837A70';
  subtitle.style.marginBottom = 'var(--spacing-lg)';

  header.appendChild(title);
  header.appendChild(subtitle);

  const filterSection = document.createElement('div');
  filterSection.style.marginBottom = 'var(--spacing-lg)';

  const searchFilter = SearchFilter({
    placeholder: 'Search restaurants...',
    filters: [
      { id: 'rating', label: 'Top Rated' },
      { id: 'fastest', label: 'Fastest Delivery' },
      { id: 'latest', label: 'Newest' }
    ],
    onSearch: (query) => console.log('Search:', query),
    onFilterChange: (filters) => console.log('Filters:', filters)
  });

  filterSection.appendChild(searchFilter);
  header.appendChild(filterSection);
  container.appendChild(header);

  const mockRestaurants = [
    { name: 'KY Burger Palace', rating: 4.8, delivery: '25-30 min', minOrder: 'UGX 10,000', img: '/resources/assets/images/placeholder/food/food-burger.jpg' },
    { name: 'Pizza Haven', rating: 4.6, delivery: '30-40 min', minOrder: 'UGX 15,000', img: '/resources/assets/images/placeholder/food/food-pizza.jpg' },
    { name: 'Fresh Salad Bar', rating: 4.9, delivery: '20-25 min', minOrder: 'UGX 8,000', img: '/resources/assets/images/placeholder/food/food-salad.jpg' },
    { name: 'Pasta Perfetto', rating: 4.7, delivery: '25-35 min', minOrder: 'UGX 12,000', img: '/resources/assets/images/placeholder/food/food-pasta.jpg' },
    { name: 'Sushi Deluxe', rating: 4.5, delivery: '35-45 min', minOrder: 'UGX 20,000', img: '/resources/assets/images/placeholder/food/food-sushi.jpg' },
    { name: 'Sweet Treats Bakery', rating: 4.9, delivery: '15-20 min', minOrder: 'UGX 5,000', img: '/resources/assets/images/placeholder/food/food-dessert.jpg' },
  ];

  const grid = document.createElement('div');
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
  grid.style.gap = 'var(--spacing-lg)';
  grid.style.maxWidth = '1200px';
  grid.style.margin = '0 auto';

  mockRestaurants.forEach(restaurant => {
    const content = document.createElement('div');
    const img = document.createElement('img');
    img.src = restaurant.img;
    img.alt = restaurant.name;
    img.style.width = '100%';
    img.style.height = '200px';
    img.style.objectFit = 'cover';
    img.style.borderRadius = 'var(--radius-md)';
    img.style.marginBottom = 'var(--spacing-sm)';

    const nameRow = document.createElement('div');
    nameRow.style.display = 'flex';
    nameRow.style.justifyContent = 'space-between';
    nameRow.style.alignItems = 'flex-start';
    nameRow.style.marginBottom = 'var(--spacing-sm)';

    const name = document.createElement('h3');
    name.textContent = restaurant.name;
    name.style.margin = '0';
    name.style.fontSize = '1.125rem';
    name.style.color = 'var(--color-neutral-brown)';

    const rating = document.createElement('span');
    rating.textContent = `★ ${restaurant.rating}`;
    rating.style.color = 'var(--color-primary-yellow)';
    rating.style.fontWeight = '600';

    nameRow.appendChild(name);
    nameRow.appendChild(rating);
    content.appendChild(img);
    content.appendChild(nameRow);

    const details = document.createElement('div');
    details.style.display = 'flex';
    details.style.gap = 'var(--spacing-md)';
    details.style.fontSize = '0.8125rem';
    details.style.color = '#837A70';

    const deliveryTime = document.createElement('span');
    deliveryTime.textContent = restaurant.delivery;

    const minOrder = document.createElement('span');
    minOrder.textContent = `Min: ${restaurant.minOrder}`;

    details.appendChild(deliveryTime);
    details.appendChild(minOrder);
    content.appendChild(details);

    const card = Card({
      children: content,
      padding: 'md',
      hoverable: true,
      clickable: true,
      onClick: () => window.location.hash = '#/restaurant-detail'
    });

    grid.appendChild(card);
  });

  container.appendChild(grid);
  return container;
}
