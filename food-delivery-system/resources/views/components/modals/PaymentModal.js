/**
 * KY Food Delivery System
 * Component: PaymentModal
 *
 * Modal for selecting and processing payment methods.
 *
 * @param {Object} options
 * @param {number} [options.amount] - Payment amount
 * @param {Array} [options.paymentMethods] - Array of payment methods {id, type, label, icon}
 * @param {Function} [options.onPay] - Callback with selected method
 * @param {Function} [options.onCancel] - Callback when cancelled
 * @returns {HTMLDivElement}
 */

import { Button } from '../common/Button.js';
import { Modal } from '../common/Modal.js';
import { Spinner } from '../common/Spinner.js';

export function PaymentModal({
  amount = 0,
  paymentMethods = [],
  onPay = null,
  onCancel = null,
} = {}) {
  const content = document.createElement('div');
  content.className = 'payment-modal__content';

  const header = document.createElement('div');
  header.className = 'payment-modal__header';

  const title = document.createElement('h3');
  title.className = 'payment-modal__title';
  title.textContent = 'Choose Payment Method';
  header.appendChild(title);

  const amountDisplay = document.createElement('div');
  amountDisplay.className = 'payment-modal__amount';
  amountDisplay.textContent = `Total: $${(amount || 0).toFixed(2)}`;
  header.appendChild(amountDisplay);

  content.appendChild(header);

  if (paymentMethods.length === 0) {
    const empty = document.createElement('p');
    empty.className = 'payment-modal__empty';
    empty.textContent = 'No payment methods available';
    content.appendChild(empty);
  } else {
    const methods = document.createElement('div');
    methods.className = 'payment-modal__methods';

    paymentMethods.forEach((method) => {
      const methodOption = document.createElement('div');
      methodOption.className = 'payment-method-option';

      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'payment-method';
      radio.value = method.id;
      radio.className = 'payment-method-option__input';

      const label = document.createElement('label');
      label.className = 'payment-method-option__label';

      if (method.icon) {
        const iconSpan = document.createElement('span');
        iconSpan.className = 'payment-method-option__icon';
        iconSpan.innerHTML = method.icon;
        label.appendChild(iconSpan);
      }

      const text = document.createElement('span');
      text.className = 'payment-method-option__text';
      text.textContent = method.label;
      label.appendChild(text);

      label.appendChild(radio);
      methodOption.appendChild(label);
      methods.appendChild(methodOption);
    });

    content.appendChild(methods);
  }

  const actions = document.createElement('div');
  actions.className = 'payment-modal__actions';

  let isProcessing = false;

  const cancelBtn = Button({
    label: 'Cancel',
    variant: 'outline',
    size: 'md',
    onClick: () => {
      if (!isProcessing) {
        if (onCancel) onCancel();
        modal.close();
      }
    },
  });

  const payBtn = Button({
    label: 'Pay Now',
    variant: 'primary',
    size: 'md',
    onClick: () => {
      const selected = content.querySelector('input[name="payment-method"]:checked');
      if (selected && onPay && !isProcessing) {
        isProcessing = true;
        payBtn.disabled = true;
        payBtn.classList.add('btn--loading');
        onPay(selected.value);
      }
    },
  });

  actions.appendChild(cancelBtn);
  actions.appendChild(payBtn);
  content.appendChild(actions);

  const modal = Modal({
    content,
    onClose: onCancel,
  });

  modal.className = 'payment-modal';

  return modal;
}
