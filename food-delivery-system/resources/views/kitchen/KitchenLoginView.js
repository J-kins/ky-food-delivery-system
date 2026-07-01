/**
 * KY Food Delivery System
 * View: Kitchen Login
 */
import { LoginForm } from '../components/forms/LoginForm.js';
import { Card } from '../components/common/Card.js';

export function KitchenLoginView() {
  const container = document.createElement('div');
  container.className = 'kitchen-login-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.padding = 'var(--spacing-xxl) var(--spacing-md)';
  container.style.minHeight = '100vh';
  container.style.backgroundColor = '#DC4024';

  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '400px';

  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';
  header.style.color = 'var(--color-white)';

  const title = document.createElement('h1');
  title.textContent = 'Kitchen Portal';
  title.style.margin = '0 0 var(--spacing-sm) 0';
  title.style.color = 'var(--color-white)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Staff Login';
  subtitle.style.margin = '0';
  subtitle.style.fontSize = '1rem';

  header.appendChild(title);
  header.appendChild(subtitle);
  formWrapper.appendChild(header);

  const form = LoginForm({
    onSubmit: (data) => {
      window.location.hash = '#/kitchen-dashboard';
    }
  });

  const card = Card({
    children: form,
    padding: 'xl',
    shadow: 'lg'
  });

  formWrapper.appendChild(card);
  container.appendChild(formWrapper);
  return container;
}
