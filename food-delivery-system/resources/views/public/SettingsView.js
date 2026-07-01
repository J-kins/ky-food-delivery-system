/**
 * KY Food Delivery System
 * View: Settings
 */
import { Button } from '../components/common/Button.js';
import { Card } from '../components/common/Card.js';

export function SettingsView() {
  const container = document.createElement('div');
  container.className = 'settings-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '700px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Settings';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const sections = [
    { title: 'Account', items: ['Email Notifications', 'SMS Alerts', 'Push Notifications'] },
    { title: 'Preferences', items: ['Language', 'Currency', 'Theme'] },
    { title: 'Security', items: ['Change Password', 'Two-Factor Authentication'] }
  ];

  sections.forEach(section => {
    const sectionTitle = document.createElement('h2');
    sectionTitle.textContent = section.title;
    sectionTitle.style.marginBottom = 'var(--spacing-lg)';
    sectionTitle.style.fontSize = '1.125rem';
    sectionTitle.style.color = 'var(--color-neutral-brown)';

    container.appendChild(sectionTitle);

    section.items.forEach(item => {
      const itemDiv = document.createElement('div');
      itemDiv.style.display = 'flex';
      itemDiv.style.justifyContent = 'space-between';
      itemDiv.style.alignItems = 'center';
      itemDiv.style.padding = 'var(--spacing-md)';
      itemDiv.style.borderBottom = '1px solid #E8D7B5';

      const label = document.createElement('span');
      label.textContent = item;
      label.style.color = 'var(--color-neutral-brown)';

      const toggle = document.createElement('input');
      toggle.type = 'checkbox';
      toggle.checked = true;
      toggle.style.width = '24px';
      toggle.style.height = '24px';
      toggle.style.cursor = 'pointer';

      itemDiv.appendChild(label);
      itemDiv.appendChild(toggle);
      container.appendChild(itemDiv);
    });
  });

  const logoutBtn = Button({ label: 'Logout', variant: 'danger', size: 'lg' });
  logoutBtn.style.width = '100%';
  logoutBtn.style.marginTop = 'var(--spacing-xl)';
  logoutBtn.onclick = () => {
    alert('Logged out successfully');
    window.location.hash = '#/login';
  };

  container.appendChild(logoutBtn);
  return container;
}
