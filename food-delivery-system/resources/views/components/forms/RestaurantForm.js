/**
 * KY Food Delivery System
 * Component: RestaurantForm
 *
 * Form for creating and editing restaurant information.
 *
 * @param {Object} options
 * @param {Object} [options.initialData] - Pre-filled form data
 * @param {Function} [options.onSubmit] - Callback with restaurant data
 * @returns {HTMLFormElement}
 */

import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function RestaurantForm({ initialData = {}, onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'restaurant-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = initialData.id ? 'Edit Restaurant' : 'Register Restaurant';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  const nameInput = Input({
    name: 'name',
    label: 'Restaurant Name',
    placeholder: 'Enter restaurant name',
    required: true,
    value: initialData.name || '',
  });
  form.appendChild(nameInput);

  const cuisineInput = Input({
    name: 'cuisine',
    label: 'Cuisine Type',
    placeholder: 'e.g., Italian, Asian',
    required: true,
    value: initialData.cuisine || '',
  });
  form.appendChild(cuisineInput);

  const row = document.createElement('div');
  row.style.display = 'flex';
  row.style.gap = 'var(--spacing-md)';

  const phoneInput = Input({
    name: 'phone',
    type: 'tel',
    label: 'Phone Number',
    placeholder: '+1 (555) 123-4567',
    required: true,
    value: initialData.phone || '',
  });
  phoneInput.style.flex = '1';

  const emailInput = Input({
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'contact@restaurant.com',
    required: true,
    value: initialData.email || '',
  });
  emailInput.style.flex = '1';

  row.appendChild(phoneInput);
  row.appendChild(emailInput);
  form.appendChild(row);

  const addressInput = Input({
    name: 'address',
    label: 'Street Address',
    placeholder: 'Enter full address',
    required: true,
    value: initialData.address || '',
  });
  form.appendChild(addressInput);

  const hoursRow = document.createElement('div');
  hoursRow.style.display = 'flex';
  hoursRow.style.gap = 'var(--spacing-md)';

  const openingInput = Input({
    name: 'opening',
    type: 'time',
    label: 'Opening Time',
    value: initialData.opening || '',
  });
  openingInput.style.flex = '1';

  const closingInput = Input({
    name: 'closing',
    type: 'time',
    label: 'Closing Time',
    value: initialData.closing || '',
  });
  closingInput.style.flex = '1';

  hoursRow.appendChild(openingInput);
  hoursRow.appendChild(closingInput);
  form.appendChild(hoursRow);

  const submitBtn = Button({
    label: initialData.id ? 'Update Restaurant' : 'Register Restaurant',
    type: 'submit',
    variant: 'primary',
    size: 'lg',
  });
  submitBtn.style.marginTop = 'var(--spacing-sm)';
  form.appendChild(submitBtn);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({
        id: initialData.id,
        name: nameInput.getValue(),
        cuisine: cuisineInput.getValue(),
        phone: phoneInput.getValue(),
        email: emailInput.getValue(),
        address: addressInput.getValue(),
        opening: openingInput.getValue(),
        closing: closingInput.getValue(),
      });
    }
  });

  return form;
}
