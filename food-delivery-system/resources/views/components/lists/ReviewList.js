/**
 * KY Food Delivery System
 * Component: ReviewList
 *
 * Renders a list of customer reviews with ratings, text, and user info.
 *
 * @param {Object} options
 * @param {Array} [options.reviews] - Array of review objects with id, author, rating, text, date, etc.
 * @param {Function} [options.onHelpful] - Callback when marking review as helpful
 * @returns {HTMLDivElement}
 */

import { Rating } from '../common/Rating.js';
import { Avatar } from '../common/Avatar.js';

export function ReviewList({ reviews = [], onHelpful = null } = {}) {
  const container = document.createElement('div');
  container.className = 'review-list';

  if (reviews.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'review-list__empty';
    empty.textContent = 'No reviews yet';
    container.appendChild(empty);
    return container;
  }

  reviews.forEach((review) => {
    const item = document.createElement('div');
    item.className = 'review-item';

    const header = document.createElement('div');
    header.className = 'review-item__header';

    const author = document.createElement('div');
    author.className = 'review-item__author';

    const avatar = Avatar({
      name: review.author || 'User',
      src: review.avatar,
      size: 'sm',
    });
    avatar.className = 'review-item__avatar';
    author.appendChild(avatar);

    const authorInfo = document.createElement('div');
    authorInfo.className = 'review-item__author-info';

    const authorName = document.createElement('h4');
    authorName.className = 'review-item__author-name';
    authorName.textContent = review.author || 'Anonymous';
    authorInfo.appendChild(authorName);

    const date = document.createElement('span');
    date.className = 'review-item__date';
    date.textContent = formatDate(review.date);
    authorInfo.appendChild(date);

    author.appendChild(authorInfo);
    header.appendChild(author);

    const rating = Rating({
      value: review.rating || 5,
      readonly: true,
    });
    rating.className = 'review-item__rating';
    header.appendChild(rating);

    item.appendChild(header);

    const body = document.createElement('div');
    body.className = 'review-item__body';

    const text = document.createElement('p');
    text.className = 'review-item__text';
    text.textContent = review.text;
    body.appendChild(text);

    item.appendChild(body);

    const footer = document.createElement('div');
    footer.className = 'review-item__footer';

    const helpful = document.createElement('button');
    helpful.className = 'review-item__helpful';
    helpful.setAttribute('type', 'button');
    helpful.innerHTML = `<span>Helpful?</span> <span class="review-item__helpful-count">${review.helpfulCount || 0}</span>`;
    helpful.addEventListener('click', () => {
      if (onHelpful) onHelpful(review.id);
    });
    footer.appendChild(helpful);

    item.appendChild(footer);
    container.appendChild(item);
  });

  return container;
}

function formatDate(dateString) {
  if (!dateString) return 'recently';
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  const days = Math.floor(diff / 86400000);

  if (days === 0) return 'today';
  if (days === 1) return 'yesterday';
  if (days < 30) return `${days} days ago`;
  if (days < 365) return `${Math.floor(days / 30)} months ago`;
  return date.toLocaleDateString();
}
