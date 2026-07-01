/**
 * KY Food Delivery System
 * Component: LoginForm
 *
 * @param {Object} options
 * @param {Function} [options.onSubmit] - Callback with { email, password }
 * @returns {HTMLFormElement}
 */
import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function LoginForm({ onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'login-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = 'Welcome Back';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  const emailInput = Input({
    name: 'email',
    type: 'email',
    label: 'Email Address',
    placeholder: 'e.g. name@example.com',
    required: true,
  });

  const passwordInput = Input({
    name: 'password',
    type: 'password',
    label: 'Password',
    placeholder: 'Enter your password',
    required: true,
  });

  const submitBtn = Button({
    label: 'Log In',
    type: 'submit',
    variant: 'primary',
    size: 'lg',
  });
  submitBtn.style.marginTop = 'var(--spacing-sm)';

  form.appendChild(emailInput);
  form.appendChild(passwordInput);
  form.appendChild(submitBtn);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({
        email: emailInput.getValue(),
        password: passwordInput.getValue(),
      });
    }
  });

  return form;
}
