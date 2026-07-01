/**
 * KY Food Delivery System
 * View: Search
 */
import { SearchFilter } from '../components/common/SearchFilter.js';
import { Card } from '../components/common/Card.js';

export function SearchView() {
  const container = document.createElement('div');
  container.className = 'search-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const header = document.createElement('section');
  header.style.marginBottom = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Search';
  title.style.marginBottom = 'var(--spacing-lg)';
  title.style.color = 'var(--color-neutral-brown)';

  header.appendChild(title);

  const searchFilter = SearchFilter({
    placeholder: 'Search foods, restaurants, or cuisines...',
    filters: [
      { id: 'foods', label: 'Foods' },
      { id: 'restaurants', label: 'Restaurants' },
      { id: 'deals', label: 'Deals' }
    ]
  });

  header.appendChild(searchFilter);
  container.appendChild(header);

  const results = document.createElement('section');
  results.style.display = 'grid';
  results.style.gridTemplateColumns = 'repeat(auto-fill, minmax(280px, 1fr))';
  results.style.gap = 'var(--spacing-lg)';

  const mockResults = [
    { type: 'food', name: 'Spicy Burger', restaurant: 'KY Burger Palace', price: 'UGX 17,000' },
    { type: 'food', name: 'Pepperoni Pizza', restaurant: 'Pizza Haven', price: 'UGX 35,000' },
    { type: 'restaurant', name: 'KY Burger Palace', rating: 4.8, delivery: '25-30 min' },
    { type: 'restaurant', name: 'Pizza Haven', rating: 4.6, delivery: '30-40 min' }
  ];

  mockResults.forEach(result => {
    const content = document.createElement('div');

    if (result.type === 'food') {
      const name = document.createElement('h3');
      name.textContent = result.name;
      name.style.margin = '0 0 var(--spacing-sm) 0';
      name.style.color = 'var(--color-neutral-brown)';

      const restaurant = document.createElement('p');
      restaurant.textContent = result.restaurant;
      restaurant.style.margin = '0 0 var(--spacing-sm) 0';
      restaurant.style.fontSize = '0.875rem';
      restaurant.style.color = '#837A70';

      const price = document.createElement('p');
      price.textContent = result.price;
      price.style.margin = '0';
      price.style.color = 'var(--color-primary-green)';
      price.style.fontWeight = '600';

      content.appendChild(name);
      content.appendChild(restaurant);
      content.appendChild(price);
    } else {
      const name = document.createElement('h3');
      name.textContent = result.name;
      name.style.margin = '0 0 var(--spacing-sm) 0';
      name.style.color = 'var(--color-neutral-brown)';

      const info = document.createElement('div');
      info.style.display = 'flex';
      info.style.gap = 'var(--spacing-md)';
      info.style.fontSize = '0.875rem';
      info.style.color = '#837A70';

      const rating = document.createElement('span');
      rating.textContent = `★ ${result.rating}`;
      rating.style.color = 'var(--color-primary-yellow)';

      const delivery = document.createElement('span');
      delivery.textContent = result.delivery;

      info.appendChild(rating);
      info.appendChild(delivery);
      content.appendChild(name);
      content.appendChild(info);
    }

    const card = Card({
      children: content,
      padding: 'md',
      hoverable: true,
      clickable: true
    });

    results.appendChild(card);
  });

  container.appendChild(results);
  return container;
}
