/**
 * KY Food Delivery System
 * View: Delivery Login
 */
import { LoginForm } from '../components/forms/LoginForm.js';
import { Card } from '../components/common/Card.js';

export function DeliveryLoginView() {
  const container = document.createElement('div');
  container.className = 'delivery-login-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.padding = 'var(--spacing-xxl) var(--spacing-md)';
  container.style.minHeight = '100vh';
  container.style.backgroundColor = '#F0C019';

  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '400px';

  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Rider Portal';
  title.style.margin = '0 0 var(--spacing-sm) 0';
  title.style.color = 'var(--color-neutral-brown)';

  const subtitle = document.createElement('p');
  subtitle.textContent = 'Delivery Partner Login';
  subtitle.style.margin = '0';
  subtitle.style.color = '#837A70';

  header.appendChild(title);
  header.appendChild(subtitle);
  formWrapper.appendChild(header);

  const form = LoginForm({
    onSubmit: (data) => {
      window.location.hash = '#/delivery-dashboard';
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
