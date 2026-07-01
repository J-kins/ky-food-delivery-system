/**
 * KY Food Delivery System
 * Admin: System Settings
 */

export function SystemSettingsView() {
  const container = document.createElement('div');
  container.className = 'system-settings-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '800px';

  const title = document.createElement('h1');
  title.textContent = 'System Settings';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const sections = [
    { title: 'General', items: ['Platform Name', 'Support Email', 'Timezone'] },
    { title: 'Commission', items: ['Restaurant Commission (%)', 'Delivery Commission (%)', 'Platform Fee'] },
    { title: 'Notifications', items: ['Email Notifications', 'SMS Alerts', 'Push Notifications'] }
  ];

  sections.forEach(section => {
    const sectionDiv = document.createElement('div');
    sectionDiv.style.marginBottom = 'var(--spacing-xl)';

    const sectionTitle = document.createElement('h2');
    sectionTitle.textContent = section.title;
    sectionTitle.style.fontSize = '1.125rem';
    sectionTitle.style.marginBottom = 'var(--spacing-lg)';
    sectionDiv.appendChild(sectionTitle);

    section.items.forEach(item => {
      const itemDiv = document.createElement('div');
      itemDiv.style.display = 'flex';
      itemDiv.style.justifyContent = 'space-between';
      itemDiv.style.padding = 'var(--spacing-md)';
      itemDiv.style.borderBottom = '1px solid #E8D7B5';

      const label = document.createElement('span');
      label.textContent = item;
      label.style.fontWeight = '500';

      const input = document.createElement('input');
      input.type = 'text';
      input.style.padding = '0.5rem';
      input.style.border = '1px solid #D0C9BF';
      input.style.borderRadius = 'var(--radius-sm)';

      itemDiv.appendChild(label);
      itemDiv.appendChild(input);
      sectionDiv.appendChild(itemDiv);
    });

    container.appendChild(sectionDiv);
  });

  const saveBtn = document.createElement('button');
  saveBtn.textContent = 'Save Settings';
  saveBtn.style.padding = 'var(--spacing-md) var(--spacing-lg)';
  saveBtn.style.backgroundColor = 'var(--color-primary-green)';
  saveBtn.style.color = 'white';
  saveBtn.style.border = 'none';
  saveBtn.style.borderRadius = 'var(--radius-md)';
  saveBtn.style.cursor = 'pointer';
  saveBtn.style.fontSize = '1rem';
  saveBtn.style.fontWeight = '600';

  container.appendChild(saveBtn);
  return container;
}
