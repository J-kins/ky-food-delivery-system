/**
 * KY Food Delivery System
 * View: Reset Password
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';
import { Input } from '../components/common/Input.js';

export function ResetPasswordView() {
  const container = document.createElement('div');
  container.className = 'reset-password-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.padding = 'var(--spacing-xxl) var(--spacing-md)';
  container.style.minHeight = '100vh';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '400px';

  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Reset Password';
  title.style.color = 'var(--color-neutral-brown)';
  title.style.marginBottom = 'var(--spacing-sm)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Enter a new password to secure your account';
  subtitle.style.color = '#837A70';
  subtitle.style.margin = '0';

  header.appendChild(title);
  header.appendChild(subtitle);

  const form = document.createElement('form');
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-lg)';

  const passwordInput = Input({
    type: 'password',
    placeholder: 'Enter new password',
    label: 'New Password',
    required: true
  });

  const confirmInput = Input({
    type: 'password',
    placeholder: 'Confirm password',
    label: 'Confirm Password',
    required: true
  });

  const submitBtn = Button({
    label: 'Reset Password',
    variant: 'primary',
    size: 'lg',
    type: 'submit'
  });
  submitBtn.style.width = '100%';

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const pwd = form.querySelector('input[type="password"]').value;
    const confirm = form.querySelectorAll('input[type="password"]')[1].value;
    if (pwd !== confirm) {
      alert('Passwords do not match!');
      return;
    }
    alert('Password reset successfully!');
    window.location.hash = '#/login';
  });

  form.appendChild(passwordInput);
  form.appendChild(confirmInput);
  form.appendChild(submitBtn);

  const card = Card({
    children: form,
    padding: 'xl',
    shadow: 'lg'
  });

  const innerForm = document.createElement('div');
  innerForm.appendChild(header);
  innerForm.appendChild(card);

  formWrapper.appendChild(innerForm);
  container.appendChild(formWrapper);
  return container;
}
