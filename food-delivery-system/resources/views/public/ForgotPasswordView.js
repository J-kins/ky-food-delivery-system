/**
 * KY Food Delivery System
 * View: Forgot Password
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';
import { Input } from '../components/common/Input.js';

export function ForgotPasswordView() {
  const container = document.createElement('div');
  container.className = 'forgot-password-view';
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
  title.textContent = 'Forgot Password?';
  title.style.color = 'var(--color-neutral-brown)';
  title.style.marginBottom = 'var(--spacing-sm)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Enter your email and we will send you a reset link';
  subtitle.style.color = '#837A70';
  subtitle.style.margin = '0';

  header.appendChild(title);
  header.appendChild(subtitle);

  const form = document.createElement('form');
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-lg)';

  const emailInput = Input({
    type: 'email',
    placeholder: 'Enter your email',
    label: 'Email Address',
    required: true
  });

  const submitBtn = Button({
    label: 'Send Reset Link',
    variant: 'primary',
    size: 'lg',
    type: 'submit'
  });
  submitBtn.style.width = '100%';

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Reset link sent to your email!');
    window.location.hash = '#/login';
  });

  form.appendChild(emailInput);
  form.appendChild(submitBtn);

  const card = Card({
    children: form,
    padding: 'xl',
    shadow: 'lg'
  });

  const innerForm = document.createElement('div');
  innerForm.appendChild(header);
  innerForm.appendChild(card);

  const backLink = document.createElement('div');
  backLink.style.textAlign = 'center';
  backLink.style.marginTop = 'var(--spacing-lg)';

  const backText = document.createElement('a');
  backText.href = '#/login';
  backText.textContent = 'Back to Login';
  backText.style.color = 'var(--color-primary-green)';
  backText.style.textDecoration = 'none';
  backText.style.fontWeight = '600';
  backText.style.cursor = 'pointer';

  backLink.appendChild(backText);
  innerForm.appendChild(backLink);

  formWrapper.appendChild(innerForm);
  container.appendChild(formWrapper);
  return container;
}
