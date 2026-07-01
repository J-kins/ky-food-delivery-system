/**
 * KY Food Delivery System
 * View: Register
 */
import { RegisterForm } from '../components/forms/RegisterForm.js';
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';

export function RegisterView() {
  const container = document.createElement('div');
  container.className = 'register-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.padding = 'var(--spacing-xxl) var(--spacing-md)';
  container.style.minHeight = '100vh';
  container.style.backgroundColor = 'var(--color-neutral-offwhite)';

  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '450px';

  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Create Account';
  title.style.color = 'var(--color-neutral-brown)';
  title.style.marginBottom = 'var(--spacing-sm)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Join KY Foods for fast, easy ordering';
  subtitle.style.color = '#837A70';
  subtitle.style.margin = '0';

  header.appendChild(title);
  header.appendChild(subtitle);
  formWrapper.appendChild(header);

  const form = RegisterForm({
    onSubmit: (data) => {
      console.log('Registration attempt:', data);
      alert(`Account created for ${data.email}!`);
      window.location.hash = '#/login';
    }
  });

  const card = Card({
    children: form,
    padding: 'xl',
    shadow: 'lg'
  });

  formWrapper.appendChild(card);

  const footer = document.createElement('div');
  footer.style.textAlign = 'center';
  footer.style.marginTop = 'var(--spacing-lg)';

  const footerText = document.createElement('p');
  footerText.textContent = 'Already have an account? ';
  footerText.style.color = '#837A70';
  footerText.style.margin = '0';

  const loginLink = document.createElement('a');
  loginLink.href = '#/login';
  loginLink.textContent = 'Login here';
  loginLink.style.color = 'var(--color-primary-green)';
  loginLink.style.textDecoration = 'none';
  loginLink.style.fontWeight = '600';
  loginLink.style.cursor = 'pointer';

  footerText.appendChild(loginLink);
  footer.appendChild(footerText);
  formWrapper.appendChild(footer);

  container.appendChild(formWrapper);
  return container;
}
