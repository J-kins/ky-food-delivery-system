/**
 * KY Food Delivery System
 * View: Login
 */
import { LoginForm } from '../components/forms/LoginForm.js';
import { Card } from '../components/common/Card.js';

export function LoginView() {
  const container = document.createElement('div');
  container.className = 'login-view';
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.padding = 'var(--spacing-xxl) var(--spacing-md)';
  container.style.minHeight = '60vh';
  
  const formWrapper = document.createElement('div');
  formWrapper.style.width = '100%';
  formWrapper.style.maxWidth = '400px';

  const form = LoginForm({
    onSubmit: (data) => {
      console.log('Login attempt:', data);
      alert(`Logging in as ${data.email}...`);
      window.location.hash = '#/';
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
