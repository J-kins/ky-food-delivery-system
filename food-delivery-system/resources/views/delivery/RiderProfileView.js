/**
 * KY Food Delivery System
 * View: Rider Profile
 */
import { Card } from '../components/common/Card.js';
import { Button } from '../components/common/Button.js';
import { Input } from '../components/common/Input.js';

export function RiderProfileView() {
  const container = document.createElement('div');
  container.className = 'rider-profile-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '800px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'My Profile';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const form = document.createElement('form');
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-lg)';

  const nameInput = Input({ type: 'text', label: 'Full Name', value: 'John Mugabe' });
  const phoneInput = Input({ type: 'tel', label: 'Phone', value: '+256 700 123456' });
  const vehicleInput = Input({ type: 'text', label: 'Vehicle', value: 'Motorcycle' });

  const saveBtn = Button({ label: 'Save Profile', variant: 'primary', size: 'lg' });
  saveBtn.style.width = '100%';
  saveBtn.onclick = (e) => {
    e.preventDefault();
    alert('Profile updated!');
  };

  form.appendChild(nameInput);
  form.appendChild(phoneInput);
  form.appendChild(vehicleInput);
  form.appendChild(saveBtn);

  const card = Card({ children: form, padding: 'xl', shadow: 'md' });
  container.appendChild(card);

  return container;
}
