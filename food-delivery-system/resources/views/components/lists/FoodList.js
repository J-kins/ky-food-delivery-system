/**
 * KY Food Delivery System
 * Component: FoodList
 *
 * Renders a grid or list of food items with images, prices, and ratings.
 *
 * @param {Object} options
 * @param {Array} [options.foods] - Array of food objects with id, name, price, rating, image, etc.
 * @param {string} [options.layout] - 'grid' or 'list' (default: 'grid')
 * @param {Function} [options.onFoodClick] - Callback when a food item is clicked
 * @returns {HTMLDivElement}
 */

import { Rating } from '../common/Rating.js';
import { Badge } from '../common/Badge.js';

export function FoodList({ foods = [], layout = 'grid', onFoodClick = null } = {}) {
  const container = document.createElement('div');
  container.className = `food-list food-list--${layout}`;

  if (foods.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'food-list__empty';
    empty.textContent = 'No food items available';
    container.appendChild(empty);
    return container;
  }

  foods.forEach((food) => {
    const card = document.createElement('div');
    card.className = 'food-card';

    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'food-card__image-wrapper';

    const image = document.createElement('div');
    image.className = 'food-card__image';
    image.style.backgroundImage = `url('${food.image || '/resources/assets/images/placeholder/food.jpg'}')`;
    imageWrapper.appendChild(image);

    if (food.badge) {
      const badge = Badge({
        label: food.badge,
        variant: food.badgeVariant || 'success',
      });
      badge.className = 'food-card__badge';
      imageWrapper.appendChild(badge);
    }

    card.appendChild(imageWrapper);

    const content = document.createElement('div');
    content.className = 'food-card__content';

    const name = document.createElement('h4');
    name.className = 'food-card__name';
    name.textContent = food.name;
    content.appendChild(name);

    const description = document.createElement('p');
    description.className = 'food-card__description';
    description.textContent = food.description || '';
    content.appendChild(description);

    const footer = document.createElement('div');
    footer.className = 'food-card__footer';

    const price = document.createElement('span');
    price.className = 'food-card__price';
    price.textContent = `$${(food.price || 0).toFixed(2)}`;
    footer.appendChild(price);

    const rating = Rating({
      value: food.rating || 4.0,
      count: food.reviewCount || 0,
      readonly: true,
    });
    rating.className = 'food-card__rating';
    footer.appendChild(rating);

    content.appendChild(footer);
    card.appendChild(content);

    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
      if (onFoodClick) onFoodClick(food.id);
    });

    container.appendChild(card);
  });

  return container;
}
