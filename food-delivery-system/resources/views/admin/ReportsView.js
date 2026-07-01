export function ReportsView() {
  const container = document.createElement('div');
  container.style.padding = 'var(--spacing-xl)';
  const title = document.createElement('h1');
  title.textContent = 'Reports';
  container.appendChild(title);
  return container;
}
