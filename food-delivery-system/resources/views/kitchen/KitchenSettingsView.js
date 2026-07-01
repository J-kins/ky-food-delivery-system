/**
 * KY Food Delivery System
 * View: Kitchen Settings
 */
import { Button } from '../components/common/Button.js';
import { Input } from '../components/common/Input.js';

export function KitchenSettingsView() {
  const container = document.createElement('div');
  container.className = 'kitchen-settings-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '700px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Kitchen Settings';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const form = document.createElement('form');
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-lg)';

  const kitchenName = Input({ type: 'text', label: 'Kitchen Name', value: 'Main Kitchen' });
  const avgPrepTime = Input({ type: 'number', label: 'Avg Prep Time (min)', value: '20' });

  const saveBtn = Button({ label: 'Save Settings', variant: 'primary', size: 'lg' });
  saveBtn.style.width = '100%';
  saveBtn.onclick = (e) => {
    e.preventDefault();
    alert('Settings saved!');
  };

  const logoutBtn = Button({ label: 'Logout', variant: 'danger', size: 'lg' });
  logoutBtn.style.width = '100%';
  logoutBtn.onclick = () => window.location.hash = '#/kitchen-login';

  form.appendChild(kitchenName);
  form.appendChild(avgPrepTime);
  form.appendChild(saveBtn);
  form.appendChild(logoutBtn);

  container.appendChild(form);
  return container;
}
