/**
 * KY Food Delivery System
 * View: Favorites
 */
import { RestaurantList } from '../components/lists/RestaurantList.js';

export function FavoritesView() {
  const container = document.createElement('div');
  container.className = 'favorites-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1200px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Favorite Restaurants';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const list = RestaurantList({
    restaurants: [
      { name: 'KY Burger Palace', rating: 4.8, delivery: '25-30 min', minOrder: 'UGX 10,000' },
      { name: 'Pizza Haven', rating: 4.6, delivery: '30-40 min', minOrder: 'UGX 15,000' }
    ]
  });

  container.appendChild(list);
  return container;
}
