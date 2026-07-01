/**
 * KY Food Delivery System
 * Component: Modal
 *
 * A fully accessible overlay dialog with focus trapping.
 *
 * @param {Object}      options
 * @param {string}      options.title         - Modal heading (required)
 * @param {HTMLElement|HTMLElement[]} [options.body] - Content elements
 * @param {HTMLElement[]}[options.actions]    - Footer action buttons
 * @param {boolean}     [options.closable]    - Show X button and allow Escape to close (default: true)
 * @param {string}      [options.size]        - 'sm' | 'md' | 'lg' | 'full' (default: 'md')
 * @param {string}      [options.id]          - Optional id
 * @param {Function}    [options.onClose]     - Called when modal is closed
 * @returns {{ el: HTMLDivElement, open: Function, close: Function }}
 *
 * Usage:
 *   import { Modal } from './components/common/Modal.js';
 *   const { el, open, close } = Modal({ title: 'Confirm Order', body: [...], actions: [okBtn] });
 *   document.body.appendChild(el);
 *   open();
 */

const CLOSE_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;

export function Modal({
  title = '',
  body = [],
  actions = [],
  closable = true,
  size = 'md',
  id = null,
  onClose = null,
} = {}) {
  // Overlay
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-labelledby', id ? `${id}-title` : 'modal-title');
  overlay.style.display = 'none';
  if (id) overlay.id = id;

  // Dialog
  const dialog = document.createElement('div');
  dialog.className = ['modal', `modal--${size}`].join(' ');

  // Header
  const header = document.createElement('div');
  header.className = 'modal__header';

  const titleEl = document.createElement('h2');
  titleEl.className = 'modal__title';
  titleEl.id = id ? `${id}-title` : 'modal-title';
  titleEl.textContent = title;
  header.appendChild(titleEl);

  if (closable) {
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'modal__close';
    closeBtn.setAttribute('aria-label', 'Close dialog');
    closeBtn.innerHTML = CLOSE_ICON;
    closeBtn.addEventListener('click', close);
    header.appendChild(closeBtn);
  }

  dialog.appendChild(header);

  // Body
  const bodyEl = document.createElement('div');
  bodyEl.className = 'modal__body';
  const bodyChildren = Array.isArray(body) ? body : [body];
  bodyChildren.forEach((child) => {
    if (child instanceof HTMLElement) bodyEl.appendChild(child);
  });
  dialog.appendChild(bodyEl);

  // Footer
  if (actions.length) {
    const footer = document.createElement('div');
    footer.className = 'modal__footer';
    actions.forEach((action) => {
      if (action instanceof HTMLElement) footer.appendChild(action);
    });
    dialog.appendChild(footer);
  }

  overlay.appendChild(dialog);

  // Close on backdrop click
  if (closable) {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });
  }

  // Keyboard
  function onKeydown(e) {
    if (e.key === 'Escape' && closable) close();
    if (e.key === 'Tab') trapFocus(e, overlay);
  }

  function open() {
    overlay.style.display = 'flex';
    overlay.classList.add('modal-overlay--visible');
    document.addEventListener('keydown', onKeydown);
    // Focus first focusable
    const focusable = overlay.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusable.length) focusable[0].focus();
  }

  function close() {
    overlay.classList.remove('modal-overlay--visible');
    overlay.classList.add('modal-overlay--exiting');
    overlay.addEventListener('animationend', () => {
      overlay.style.display = 'none';
      overlay.classList.remove('modal-overlay--exiting');
      document.removeEventListener('keydown', onKeydown);
      if (onClose) onClose();
    }, { once: true });
  }

  function trapFocus(e, container) {
    const focusable = Array.from(container.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'));
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus(); }
    } else {
      if (document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }

  return { el: overlay, open, close };
}
