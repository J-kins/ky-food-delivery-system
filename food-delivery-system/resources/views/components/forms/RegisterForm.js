/**
 * KY Food Delivery System
 * Component: RegisterForm
 *
 * @param {Object} options
 * @param {Function} [options.onSubmit] - Callback with user details
 * @returns {HTMLFormElement}
 */
import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function RegisterForm({ onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'register-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = 'Create an Account';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  // Row for first / last name
  const nameRow = document.createElement('div');
  nameRow.style.display = 'flex';
  nameRow.style.gap = 'var(--spacing-md)';
  
  const fnInput = Input({ name: 'firstName', label: 'First Name', required: true });
  const lnInput = Input({ name: 'lastName', label: 'Last Name', required: true });
  fnInput.style.flex = '1';
  lnInput.style.flex = '1';
  
  nameRow.appendChild(fnInput);
  nameRow.appendChild(lnInput);
  form.appendChild(nameRow);

  const emailInput = Input({
    name: 'email',
    type: 'email',
    label: 'Email Address',
    required: true,
  });

  const phoneInput = Input({
    name: 'phone',
    type: 'tel',
    label: 'Phone Number',
    required: true,
  });

  const passwordInput = Input({
    name: 'password',
    type: 'password',
    label: 'Password',
    required: true,
  });

  const submitBtn = Button({
    label: 'Create Account',
    type: 'submit',
    variant: 'primary',
    size: 'lg',
  });
  submitBtn.style.marginTop = 'var(--spacing-sm)';

  form.appendChild(emailInput);
  form.appendChild(phoneInput);
  form.appendChild(passwordInput);
  form.appendChild(submitBtn);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({
        firstName: fnInput.getValue(),
        lastName: lnInput.getValue(),
        email: emailInput.getValue(),
        phone: phoneInput.getValue(),
        password: passwordInput.getValue(),
      });
    }
  });

  return form;
}
