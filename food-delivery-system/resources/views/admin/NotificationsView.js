export function NotificationsView() {
  const container = document.createElement('div');
  container.style.padding = 'var(--spacing-xl)';
  const title = document.createElement('h1');
  title.textContent = 'Notifications';
  container.appendChild(title);
  return container;
}
