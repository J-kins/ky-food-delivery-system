/**
 * KY Food Delivery System
 * Component: ConfirmModal
 *
 * Generic confirmation/alert modal dialog.
 *
 * @param {Object} options
 * @param {string} [options.title] - Modal title
 * @param {string} [options.message] - Modal message/body text
 * @param {string} [options.confirmLabel] - Text for confirm button (default: 'Confirm')
 * @param {string} [options.cancelLabel] - Text for cancel button (default: 'Cancel')
 * @param {string} [options.confirmVariant] - Button variant for confirm (default: 'primary')
 * @param {Function} [options.onConfirm] - Callback when confirmed
 * @param {Function} [options.onCancel] - Callback when cancelled
 * @param {boolean} [options.isOpen] - Initial open state
 * @returns {HTMLDivElement}
 */

import { Button } from '../common/Button.js';
import { Modal } from '../common/Modal.js';

export function ConfirmModal({
  title = 'Confirm',
  message = 'Are you sure?',
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  confirmVariant = 'primary',
  onConfirm = null,
  onCancel = null,
  isOpen = false,
} = {}) {
  const content = document.createElement('div');
  content.className = 'confirm-modal__content';

  if (title) {
    const titleEl = document.createElement('h3');
    titleEl.className = 'confirm-modal__title';
    titleEl.textContent = title;
    content.appendChild(titleEl);
  }

  const messageEl = document.createElement('p');
  messageEl.className = 'confirm-modal__message';
  messageEl.textContent = message;
  content.appendChild(messageEl);

  const actions = document.createElement('div');
  actions.className = 'confirm-modal__actions';

  const cancelBtn = Button({
    label: cancelLabel,
    variant: 'outline',
    size: 'md',
    onClick: () => {
      if (onCancel) onCancel();
      modal.close();
    },
  });

  const confirmBtn = Button({
    label: confirmLabel,
    variant: confirmVariant,
    size: 'md',
    onClick: () => {
      if (onConfirm) onConfirm();
      modal.close();
    },
  });

  actions.appendChild(cancelBtn);
  actions.appendChild(confirmBtn);
  content.appendChild(actions);

  const modal = Modal({
    content,
    isOpen,
    onClose: onCancel,
  });

  modal.className = 'confirm-modal';

  return modal;
}
