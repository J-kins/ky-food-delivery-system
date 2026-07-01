/**
 * KY Food Delivery System
 * Component: SupportTicketForm
 *
 * Form for creating support/help tickets.
 *
 * @param {Object} options
 * @param {Function} [options.onSubmit] - Callback with ticket data
 * @returns {HTMLFormElement}
 */

import { Input } from '../common/Input.js';
import { Button } from '../common/Button.js';

export function SupportTicketForm({ onSubmit } = {}) {
  const form = document.createElement('form');
  form.className = 'support-ticket-form';
  form.style.display = 'flex';
  form.style.flexDirection = 'column';
  form.style.gap = 'var(--spacing-md)';

  const title = document.createElement('h2');
  title.textContent = 'Contact Support';
  title.style.marginBottom = 'var(--spacing-sm)';
  form.appendChild(title);

  const subjectInput = Input({
    name: 'subject',
    label: 'Subject',
    placeholder: 'What is your issue?',
    required: true,
  });
  form.appendChild(subjectInput);

  const categorySelect = document.createElement('select');
  categorySelect.className = 'form-field__input';
  categorySelect.name = 'category';
  categorySelect.required = true;
  categorySelect.style.marginBottom = 'var(--spacing-sm)';

  const categoryLabel = document.createElement('label');
  categoryLabel.className = 'form-field__label';
  categoryLabel.textContent = 'Category';
  form.appendChild(categoryLabel);

  const categories = [
    { value: 'order', label: 'Order Issue' },
    { value: 'delivery', label: 'Delivery Issue' },
    { value: 'payment', label: 'Payment Issue' },
    { value: 'account', label: 'Account Issue' },
    { value: 'other', label: 'Other' },
  ];

  categories.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat.value;
    option.textContent = cat.label;
    categorySelect.appendChild(option);
  });

  form.appendChild(categorySelect);

  const prioritySelect = document.createElement('select');
  prioritySelect.className = 'form-field__input';
  prioritySelect.name = 'priority';
  prioritySelect.style.marginBottom = 'var(--spacing-sm)';

  const priorityLabel = document.createElement('label');
  priorityLabel.className = 'form-field__label';
  priorityLabel.textContent = 'Priority';
  form.appendChild(priorityLabel);

  const priorities = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
  ];

  priorities.forEach(pri => {
    const option = document.createElement('option');
    option.value = pri.value;
    option.textContent = pri.label;
    prioritySelect.appendChild(option);
  });

  form.appendChild(prioritySelect);

  const descriptionArea = document.createElement('textarea');
  descriptionArea.className = 'form-field__input';
  descriptionArea.name = 'description';
  descriptionArea.placeholder = 'Please describe your issue in detail...';
  descriptionArea.rows = 5;
  descriptionArea.required = true;
  descriptionArea.style.resize = 'vertical';
  descriptionArea.style.fontFamily = "'Poppins', sans-serif";

  const descLabel = document.createElement('label');
  descLabel.className = 'form-field__label';
  descLabel.textContent = 'Description';
  descLabel.style.marginBottom = 'var(--spacing-xs)';
  form.appendChild(descLabel);
  form.appendChild(descriptionArea);

  const contactInput = Input({
    name: 'contact',
    type: 'email',
    label: 'Contact Email',
    placeholder: 'your.email@example.com',
    required: true,
  });
  form.appendChild(contactInput);

  const submitBtn = Button({
    label: 'Submit Ticket',
    type: 'submit',
    variant: 'primary',
    size: 'lg',
  });
  submitBtn.style.marginTop = 'var(--spacing-sm)';
  form.appendChild(submitBtn);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({
        subject: subjectInput.getValue(),
        category: categorySelect.value,
        priority: prioritySelect.value,
        description: descriptionArea.value.trim(),
        contact: contactInput.getValue(),
      });
    }
  });

  return form;
}
