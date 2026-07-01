/**
 * KY Food Delivery System
 * Component: ReviewModal
 *
 * Modal for submitting reviews and ratings for orders/restaurants.
 *
 * @param {Object} options
 * @param {string} [options.title] - Modal title
 * @param {string} [options.itemName] - Name of item being reviewed
 * @param {Function} [options.onSubmit] - Callback with {rating, text}
 * @param {Function} [options.onCancel] - Callback when cancelled
 * @returns {HTMLDivElement}
 */

import { Button } from '../common/Button.js';
import { Modal } from '../common/Modal.js';
import { Input } from '../common/Input.js';

export function ReviewModal({
  title = 'Leave a Review',
  itemName = '',
  onSubmit = null,
  onCancel = null,
} = {}) {
  const content = document.createElement('div');
  content.className = 'review-modal__content';

  const header = document.createElement('div');
  header.className = 'review-modal__header';

  const titleEl = document.createElement('h3');
  titleEl.className = 'review-modal__title';
  titleEl.textContent = title;
  header.appendChild(titleEl);

  if (itemName) {
    const item = document.createElement('p');
    item.className = 'review-modal__item-name';
    item.textContent = itemName;
    header.appendChild(item);
  }

  content.appendChild(header);

  const form = document.createElement('form');
  form.className = 'review-modal__form';

  const ratingSection = document.createElement('div');
  ratingSection.className = 'review-modal__rating-section';

  const ratingLabel = document.createElement('label');
  ratingLabel.className = 'review-modal__rating-label';
  ratingLabel.textContent = 'Rating';
  ratingSection.appendChild(ratingLabel);

  const ratingStars = document.createElement('div');
  ratingStars.className = 'review-modal__rating-stars';

  let selectedRating = 0;

  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('button');
    star.type = 'button';
    star.className = 'review-modal__star';
    star.setAttribute('data-rating', i);
    star.innerHTML = '★';

    star.addEventListener('click', (e) => {
      e.preventDefault();
      selectedRating = i;
      updateStars();
    });

    star.addEventListener('mouseenter', () => {
      updateStarsHover(i);
    });

    ratingStars.appendChild(star);
  }

  ratingStars.addEventListener('mouseleave', updateStars);

  function updateStars() {
    const stars = ratingStars.querySelectorAll('.review-modal__star');
    stars.forEach((star, idx) => {
      if (idx < selectedRating) {
        star.classList.add('review-modal__star--active');
      } else {
        star.classList.remove('review-modal__star--active');
      }
    });
  }

  function updateStarsHover(count) {
    const stars = ratingStars.querySelectorAll('.review-modal__star');
    stars.forEach((star, idx) => {
      if (idx < count) {
        star.classList.add('review-modal__star--hover');
      } else {
        star.classList.remove('review-modal__star--hover');
      }
    });
  }

  ratingSection.appendChild(ratingStars);
  form.appendChild(ratingSection);

  const textarea = document.createElement('textarea');
  textarea.className = 'review-modal__textarea';
  textarea.placeholder = 'Tell us about your experience (optional)';
  textarea.rows = 4;
  form.appendChild(textarea);

  content.appendChild(form);

  const actions = document.createElement('div');
  actions.className = 'review-modal__actions';

  const cancelBtn = Button({
    label: 'Cancel',
    variant: 'outline',
    size: 'md',
    onClick: () => {
      if (onCancel) onCancel();
      modal.close();
    },
  });

  const submitBtn = Button({
    label: 'Submit Review',
    variant: 'primary',
    size: 'md',
    onClick: () => {
      if (selectedRating === 0) {
        alert('Please select a rating');
        return;
      }
      if (onSubmit) {
        onSubmit({
          rating: selectedRating,
          text: textarea.value.trim(),
        });
      }
      modal.close();
    },
  });

  actions.appendChild(cancelBtn);
  actions.appendChild(submitBtn);
  content.appendChild(actions);

  const modal = Modal({
    content,
    onClose: onCancel,
  });

  modal.className = 'review-modal';

  return modal;
}
