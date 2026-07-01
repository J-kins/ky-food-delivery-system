/**
 * KY Food Delivery System
 * Component: PromotionForm
 *
 * Form for creating and managing promotions.
 *
 * @param {Object} options
 * @param {Function} [options.onSubmit] - Callback with promotion data
 * @returns {HTMLFormElement}
 */

import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function PromotionForm({ onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'promotion-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = 'Create Promotion';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  const codeInput = Input({
    name: 'code',
    label: 'Promo Code',
    placeholder: 'e.g., SAVE20',
    required: true,
  });
  form.appendChild(codeInput);

  const descriptionInput = Input({
    name: 'description',
    label: 'Description',
    placeholder: 'What does this promotion offer?',
    required: true,
  });
  form.appendChild(descriptionInput);

  const row = document.createElement('div');
  row.style.display = 'flex';
  row.style.gap = 'var(--spacing-md)';

  const discountInput = Input({
    name: 'discount',
    type: 'number',
    label: 'Discount (%)',
    placeholder: '20',
    required: true,
  });
  discountInput.style.flex = '1';

  const maxUsesInput = Input({
    name: 'maxUses',
    type: 'number',
    label: 'Max Uses',
    placeholder: '100',
    required: true,
  });
  maxUsesInput.style.flex = '1';

  row.appendChild(discountInput);
  row.appendChild(maxUsesInput);
  form.appendChild(row);

  const dateRow = document.createElement('div');
  dateRow.style.display = 'flex';
  dateRow.style.gap = 'var(--spacing-md)';

  const startDateInput = Input({
    name: 'startDate',
    type: 'date',
    label: 'Start Date',
    required: true,
  });
  startDateInput.style.flex = '1';

  const endDateInput = Input({
    name: 'endDate',
    type: 'date',
    label: 'End Date',
    required: true,
  });
  endDateInput.style.flex = '1';

  dateRow.appendChild(startDateInput);
  dateRow.appendChild(endDateInput);
  form.appendChild(dateRow);

  const submitBtn = Button({
    label: 'Create Promotion',
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
        code: codeInput.getValue(),
        description: descriptionInput.getValue(),
        discount: parseInt(discountInput.getValue(), 10),
        maxUses: parseInt(maxUsesInput.getValue(), 10),
        startDate: startDateInput.getValue(),
        endDate: endDateInput.getValue(),
      });
    }
  });

  return form;
}
