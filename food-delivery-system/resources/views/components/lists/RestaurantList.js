/**
 * KY Food Delivery System
 * Component: RestaurantList
 *
 * Renders a list of restaurant cards with ratings, delivery time, and cuisine info.
 *
 * @param {Object} options
 * @param {Array} [options.restaurants] - Array of restaurant objects with id, name, cuisine, rating, deliveryTime, image, etc.
 * @param {Function} [options.onRestaurantClick] - Callback when a restaurant card is clicked
 * @returns {HTMLDivElement}
 */

import { Rating } from '../common/Rating.js';
import { Badge } from '../common/Badge.js';

export function RestaurantList({ restaurants = [], onRestaurantClick = null } = {}) {
  const container = document.createElement('div');
  container.className = 'restaurant-list';

  if (restaurants.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'restaurant-list__empty';
    empty.textContent = 'No restaurants available';
    container.appendChild(empty);
    return container;
  }

  restaurants.forEach((restaurant) => {
    const card = document.createElement('div');
    card.className = 'restaurant-card';
    if (restaurant.featured) card.classList.add('restaurant-card--featured');

    const image = document.createElement('div');
    image.className = 'restaurant-card__image';
    image.style.backgroundImage = `url('${restaurant.image || '/resources/assets/images/placeholder/restaurant.jpg'}')`;
    card.appendChild(image);

    if (restaurant.discount) {
      const badge = Badge({
        label: `${restaurant.discount}% OFF`,
        variant: 'danger',
      });
      badge.className = 'restaurant-card__discount-badge';
      image.appendChild(badge);
    }

    const content = document.createElement('div');
    content.className = 'restaurant-card__content';

    const header = document.createElement('div');
    header.className = 'restaurant-card__header';

    const name = document.createElement('h3');
    name.className = 'restaurant-card__name';
    name.textContent = restaurant.name;
    header.appendChild(name);

    const rating = Rating({
      value: restaurant.rating || 4.5,
      count: restaurant.reviewCount || 0,
      readonly: true,
    });
    rating.className = 'restaurant-card__rating';
    header.appendChild(rating);

    content.appendChild(header);

    const meta = document.createElement('div');
    meta.className = 'restaurant-card__meta';

    const cuisine = document.createElement('span');
    cuisine.className = 'restaurant-card__cuisine';
    cuisine.textContent = restaurant.cuisine || 'Various';
    meta.appendChild(cuisine);

    const delivery = document.createElement('span');
    delivery.className = 'restaurant-card__delivery';
    delivery.innerHTML = `<span class="delivery-icon"></span>${restaurant.deliveryTime || '30-40'} min`;
    meta.appendChild(delivery);

    content.appendChild(meta);

    card.appendChild(content);
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
      if (onRestaurantClick) onRestaurantClick(restaurant.id);
    });

    container.appendChild(card);
  });

  return container;
}
