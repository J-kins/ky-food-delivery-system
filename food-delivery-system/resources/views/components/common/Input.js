/**
 * KY Food Delivery System
 * Component: Input
 *
 * Factory function that creates a labelled form input wrapper DOM element.
 *
 * @param {Object}   options
 * @param {string}   options.name         - Input name attribute (required)
 * @param {string}   [options.type]       - Input type (default: 'text')
 * @param {string}   [options.label]      - Visible label text
 * @param {string}   [options.placeholder]- Placeholder text
 * @param {string}   [options.value]      - Initial value
 * @param {boolean}  [options.required]   - Required attribute
 * @param {boolean}  [options.disabled]   - Disabled state
 * @param {boolean}  [options.readonly]   - Readonly state
 * @param {string}   [options.error]      - Error message string (renders error state)
 * @param {string}   [options.hint]       - Helper/hint text shown below input
 * @param {string}   [options.leadIcon]   - Raw SVG for left side icon
 * @param {string}   [options.trailIcon]  - Raw SVG for right side icon
 * @param {string}   [options.id]         - Optional HTML id (auto-derived from name if omitted)
 * @param {string}   [options.className]  - Additional CSS classes on the wrapper
 * @param {Function} [options.onInput]    - Input event handler
 * @param {Function} [options.onChange]   - Change event handler
 * @returns {HTMLDivElement} Wrapper div containing label + input + error/hint text
 *
 * Usage:
 *   import { Input } from './components/common/Input.js';
 *   form.appendChild(Input({ name: 'email', type: 'email', label: 'Email address', required: true }));
 */

export function Input({
  name,
  type = 'text',
  label = '',
  placeholder = '',
  value = '',
  required = false,
  disabled = false,
  readonly = false,
  error = '',
  hint = '',
  leadIcon = null,
  trailIcon = null,
  id = null,
  className = '',
  onInput = null,
  onChange = null,
} = {}) {
  const inputId = id || `input-${name}`;

  // Wrapper
  const wrapper = document.createElement('div');
  wrapper.className = ['form-field', error ? 'form-field--error' : '', className].filter(Boolean).join(' ');

  // Label
  if (label) {
    const lbl = document.createElement('label');
    lbl.htmlFor = inputId;
    lbl.className = 'form-field__label';
    lbl.textContent = label;
    if (required) {
      const req = document.createElement('span');
      req.className = 'form-field__required';
      req.textContent = ' *';
      req.setAttribute('aria-hidden', 'true');
      lbl.appendChild(req);
    }
    wrapper.appendChild(lbl);
  }

  // Input row
  const row = document.createElement('div');
  row.className = 'form-field__row';

  if (leadIcon) {
    const iconWrap = document.createElement('span');
    iconWrap.className = 'form-field__icon form-field__icon--lead';
    iconWrap.innerHTML = leadIcon;
    row.appendChild(iconWrap);
  }

  const input = document.createElement('input');
  input.id = inputId;
  input.name = name;
  input.type = type;
  input.placeholder = placeholder;
  input.value = value;
  input.required = required;
  input.disabled = disabled;
  input.readOnly = readonly;
  input.className = 'form-field__input';
  if (leadIcon) input.classList.add('form-field__input--lead-icon');
  if (trailIcon) input.classList.add('form-field__input--trail-icon');

  if (onInput) input.addEventListener('input', onInput);
  if (onChange) input.addEventListener('change', onChange);
  row.appendChild(input);

  if (trailIcon) {
    const iconWrap = document.createElement('span');
    iconWrap.className = 'form-field__icon form-field__icon--trail';
    iconWrap.innerHTML = trailIcon;
    row.appendChild(iconWrap);
  }

  wrapper.appendChild(row);

  // Error message
  if (error) {
    const errEl = document.createElement('p');
    errEl.className = 'form-field__error-text';
    errEl.textContent = error;
    wrapper.appendChild(errEl);
  }

  // Hint text
  if (hint && !error) {
    const hintEl = document.createElement('p');
    hintEl.className = 'form-field__hint';
    hintEl.textContent = hint;
    wrapper.appendChild(hintEl);
  }

  /** Expose helper to programmatically set error */
  wrapper.setError = (msg) => {
    input.classList.toggle('form-field__input--error', !!msg);
    wrapper.classList.toggle('form-field--error', !!msg);
    const existing = wrapper.querySelector('.form-field__error-text');
    if (msg) {
      if (existing) {
        existing.textContent = msg;
      } else {
        const errEl = document.createElement('p');
        errEl.className = 'form-field__error-text';
        errEl.textContent = msg;
        wrapper.appendChild(errEl);
      }
    } else if (existing) {
      existing.remove();
    }
  };

  /** Expose value getter */
  wrapper.getValue = () => input.value;

  return wrapper;
}
