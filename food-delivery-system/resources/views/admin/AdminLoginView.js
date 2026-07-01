/**
 * KY Food Delivery System
 * Admin: Login
 */
import { LoginForm } from '../components/forms/LoginForm.js';
import { Card } from '../components/common/Card.js';

export function AdminLoginView() {
  const container = document.createElement('div');
  container.className = 'admin-login-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.minHeight = '100vh';
  container.style.backgroundColor = 'var(--color-neutral-brown)';

  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '400px';
  formWrapper.style.margin = '0 var(--spacing-md)';

  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';
  header.style.color = 'var(--color-white)';

  const title = document.createElement('h1');
  title.textContent = 'Admin Portal';
  title.style.color = 'var(--color-white)';
  title.style.margin = '0 0 var(--spacing-sm) 0';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'System Administrator';
  subtitle.style.margin = '0';
  subtitle.style.opacity = '0.9';

  header.appendChild(title);
  header.appendChild(subtitle);
  formWrapper.appendChild(header);

  const form = LoginForm({
    onSubmit: () => window.location.hash = '#/admin-dashboard'
  });

  const card = Card({ children: form, padding: 'xl', shadow: 'lg' });
  formWrapper.appendChild(card);
  container.appendChild(formWrapper);

  return container;
}
