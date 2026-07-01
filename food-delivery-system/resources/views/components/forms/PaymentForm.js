/**
 * KY Food Delivery System
 * Component: PaymentForm
 *
 * Form for entering payment card details.
 *
 * @param {Object} options
 * @param {Function} [options.onSubmit] - Callback with payment details
 * @returns {HTMLFormElement}
 */

import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function PaymentForm({ onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'payment-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = 'Payment Details';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  const cardholderInput = Input({
    name: 'cardholder',
    label: 'Cardholder Name',
    placeholder: 'John Doe',
    required: true,
  });
  form.appendChild(cardholderInput);

  const cardNumberInput = Input({
    name: 'cardNumber',
    label: 'Card Number',
    placeholder: '1234 5678 9012 3456',
    required: true,
  });
  form.appendChild(cardNumberInput);

  const row = document.createElement('div');
  row.style.display = 'flex';
  row.style.gap = 'var(--spacing-md)';

  const expiryInput = Input({
    name: 'expiry',
    label: 'Expiry Date',
    placeholder: 'MM/YY',
    required: true,
  });
  expiryInput.style.flex = '1';

  const cvcInput = Input({
    name: 'cvc',
    label: 'CVC',
    placeholder: '123',
    type: 'password',
    required: true,
  });
  cvcInput.style.flex = '1';

  row.appendChild(expiryInput);
  row.appendChild(cvcInput);
  form.appendChild(row);

  const submitBtn = Button({
    label: 'Add Card',
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
        cardholder: cardholderInput.getValue(),
        cardNumber: cardNumberInput.getValue(),
        expiry: expiryInput.getValue(),
        cvc: cvcInput.getValue(),
      });
    }
  });

  return form;
}
