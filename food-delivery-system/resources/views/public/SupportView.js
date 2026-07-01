/**
 * KY Food Delivery System
 * View: Support
 */
import { SupportTicketForm } from '../components/forms/SupportTicketForm.js';

export function SupportView() {
  const container = document.createElement('div');
  container.className = 'support-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '800px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Support';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const form = SupportTicketForm({
    onSubmit: (data) => {
      alert('Support ticket submitted! Ticket ID: #SUP' + Date.now());
      window.location.hash = '#/profile';
    }
  });

  container.appendChild(form);
  return container;
}
